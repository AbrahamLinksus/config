from typing import Literal
from pydantic import BaseModel, conlist, Field, field_validator
from datetime import time, date, datetime, timedelta

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

class ScheduleInput(ScheduleBase):
    def calculate_timetable(self, service) -> ScheduleOutput:
        timetable = []
        current_batch = 1
        start_date = self.start_date
        send_pace = 5
        mails_to_send = len(self.recipients)
        for index, recipient_id in enumerate(self.recipients):
            schedule_list = []
            datetime_dummy = datetime(2000,1,1)
            time1 = datetime.combine(datetime_dummy,(self.schedule[0].end_time))
            time2 = datetime.combine(datetime_dummy,(self.schedule[0].start_time))
            time_diff_in_minutes = int((time1 - time2).total_seconds()/60)
            gap_inbetween = int(time_diff_in_minutes / mails_to_send)
            send_pace = min(send_pace,gap_inbetween)
            for week_schedule in self.schedule:
                email_number = week_schedule.email_number
                days_delta = (week_schedule.week - 1) * 7 + week_schedule.day_number
                date = start_date + timedelta(days=days_delta) 
                schedule_time = datetime.combine(date, week_schedule.start_time) + timedelta(minutes=5 * index)
                schedule_list.append(RecipientSchedule(email_number=email_number, send_time=schedule_time))
            detail = RecipientDetail(recipient_id=recipient_id, batch_number=current_batch, schedule=schedule_list)
            timetable.append(detail)    
        return ScheduleOutput(**self.model_dump(), timetable=timetable)
    
