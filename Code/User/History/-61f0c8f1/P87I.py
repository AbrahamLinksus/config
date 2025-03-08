from typing import Literal
from pydantic import BaseModel, conlist, Field, field_validator
from datetime import time, date, datetime, timedelta
from enum import Enum

DOW = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class WeekSchedule(BaseModel):
    email_number: int
    day: Literal['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    week: int
    start_time: time
    end_time: time
    timezone: str
    send_as_reply: bool = True

    @property
    def day_number(self):
        return DOW.index(self.day)
    
    @field_validator("end_time")
    def check_end_time(cls, v):
        time=datetime.now().time()
        if v < time:
            raise ValueError("The given end time is already over")
        return v



class ScheduleBase(BaseModel):
    campaign_id: int
    sending_account_id: int
    sending_limit: int
    schedule: conlist(WeekSchedule)
    start_date: date
    recipients: conlist(int)

    @field_validator("start_date")
    def check_date(cls, v):
        today=date.today()
        if v < today:
            raise ValueError("The given date is older than today")
        return v


class RecipientSchedule(BaseModel):
    email_number: int
    send_time: datetime

    def __eq__(self, other):
        if not isinstance(other, RecipientSchedule):
            return NotImplemented
        return (
            self.email_number == other.email_number
            and self.send_time == other.send_time
        )

    def __hash__(self):
        return hash((self.email_number, self.send_time))

class RecipientDetail(BaseModel):
    recipient_id: int
    batch_number: int
    schedule: list[RecipientSchedule]

    def __eq__(self, other):
        if not isinstance(other, RecipientDetail):
            return NotImplemented
        return (
            self.recepient_id == other.recepient_id
            and self.batch_number == other.batch_number
            and self.schedule == other.schedule
        )

    def __hash__(self):
        # Use a tuple of the fields used in equality comparison
        return hash((self.recepient_id, self.batch_number, tuple(self.schedule)))


class ScheduleOutput(ScheduleBase):
    timetable: conlist(RecipientDetail)

class SchedulingStrategy(Enum):
    SINGLE_BATCH = "single"    # Only schedule first batch
    ALL_BATCHES = "all"        # Schedule all recipients across batches
    MAX_BATCHES = "max"        # Schedule up to a maximum number of batches

class ScheduleInput(ScheduleBase):
    def calculate_timetable(self, service, strategy: SchedulingStrategy = SchedulingStrategy.ALL_BATCHES, max_batches: int = None) -> ScheduleOutput:
        if not self.recipients:
            return ScheduleOutput(**self.model_dump(), timetable=[])

        timetable = []
        current_batch = 1
        batch_start_date = self.start_date
        send_pace = 5
        remaining_recipients = self.recipients.copy()
        
        while remaining_recipients:
            # Check scheduling strategy conditions
            if strategy == SchedulingStrategy.SINGLE_BATCH and current_batch > 1:
                break
            if strategy == SchedulingStrategy.MAX_BATCHES and current_batch > max_batches:
                break

            # Get the daily capacity from the service
            capacities = service.calculate_capacity()
            if not capacities:
                raise ValueError("No capacity information available")
            
            # For the first scheduled day of this batch, get its capacity
            first_schedule = self.schedule[0]
            schedule_date = batch_start_date + timedelta(days=first_schedule.day_number)
            
            daily_capacity = next(
                (cap.capacity for cap in capacities if cap.send_date == schedule_date),
                0
            )
            
            if daily_capacity == 0:
                break
            
            # Take only as many recipients as we have capacity for
            batch_recipients = remaining_recipients[:daily_capacity]
            remaining_recipients = remaining_recipients[daily_capacity:]
            
            # Calculate time spacing for this batch
            datetime_dummy = datetime(2000, 1, 1)
            time1 = datetime.combine(datetime_dummy, first_schedule.end_time)
            time2 = datetime.combine(datetime_dummy, first_schedule.start_time)
            time_diff_in_minutes = int((time1 - time2).total_seconds()/60)
            gap_inbetween = int(time_diff_in_minutes / max(len(batch_recipients), 1))
            current_send_pace = min(send_pace, gap_inbetween)
            
            # Schedule each recipient in this batch
            for index, recipient_id in enumerate(batch_recipients):
                schedule_list = []
                
                for week_schedule in self.schedule:
                    email_number = week_schedule.email_number
                    days_delta = (week_schedule.week - 1) * 7 + week_schedule.day_number
                    schedule_date = batch_start_date + timedelta(days=days_delta)
                    base_time = datetime.combine(schedule_date, week_schedule.start_time)
                    send_time = base_time + timedelta(minutes=current_send_pace * index)
                    
                    schedule_list.append(
                        RecipientSchedule(
                            email_number=email_number,
                            send_time=send_time
                        )
                    )
                
                detail = RecipientDetail(
                    recipient_id=recipient_id,
                    batch_number=current_batch,
                    schedule=schedule_list
                )
                timetable.append(detail)
            
            # Move to next batch and update start date to next week
            current_batch += 1
            batch_start_date += timedelta(days=7)
        
        return ScheduleOutput(**self.model_dump(), timetable=timetable)
    
