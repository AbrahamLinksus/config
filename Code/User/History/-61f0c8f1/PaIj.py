from typing import Literal
from pydantic import BaseModel, conlist, Field, field_validator
from datetime import time, date, datetime

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

class Date_validator(BaseModel):
    start_date: date

    @field_validator("given_date")
    def check_date(cls, v):
        today=date.today()
        if v < today:
            raise ValueError("The given date is older than today")

class ScheduleBase(BaseModel):
    campaign_id: int
    sending_account_id: int
    sending_limit: int
    schedule: conlist(WeekSchedule)
    start_date: date
    recipients: conlist(int)


class ScheduleInput(ScheduleBase):
    pass

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
