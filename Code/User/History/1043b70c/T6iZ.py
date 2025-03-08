import pytest
from app.scheduler import Scheduler
from app.contracts import ScheduleInput, RecipientSchedule
from datetime import datetime, date
from unittest.mock import MagicMock
from app.campaign_service import CampaignService, SendCapacity
import warnings
from datetime import datetime, timedelta, time, date


def create_capacity(next_monday, days_offset, capacity) -> SendCapacity:
    return SendCapacity(
        send_date=next_monday + timedelta(days=days_offset),
        capacity=capacity
    )

def generate_dates(start_date, capacities):
    days_count = len(capacities)
    # Ensure the input date is in datetime format
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Find the next Monday
    days_until_monday = (7 - start_date.weekday()) % 7
    next_monday = start_date + timedelta(days=days_until_monday)
    
    # Generate the series of dates
    return [create_capacity(next_monday, i, capacities[i]) for i in range(days_count)]



LARGE_CAPACITIES = generate_dates(datetime.now().date(), [200 for _ in range(7*2)])

def test_scheduler_with_one_email_one_recipient():
    service = MagicMock(spec=CampaignService)
    service.calculate_capacity.return_value = LARGE_CAPACITIES
    start_date = LARGE_CAPACITIES[0].send_date
    data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
          "email_number": 1,
          "day": "wed",
          "week": 1,
          "start_time": "09:00:00",
          "end_time": "17:00:00",
          "timezone": "UTC",
          "send_as_reply": True
          }
      ],
      "start_date": start_date,
      "recipients": [12345]
    }
    input =  ScheduleInput.model_validate(data)
    output = Scheduler(service).schedule(input)

    assert(len(output.timetable) == 1)

    recipient_detail = output.timetable[0]
    assert(recipient_detail.recipient_id == 12345)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 1)
    schedule_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
    first_schedule = RecipientSchedule(email_number=1, send_time=schedule_time)
    assert(recipient_detail.schedule == [first_schedule])

def test_scheduler_with_two_email_two_recipients():
    service = MagicMock(spec=CampaignService)
    service.calculate_capacity.return_value = LARGE_CAPACITIES
    start_date = LARGE_CAPACITIES[0].send_date
    data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
            "email_number": 1,
            "day": "wed",
            "week": 1,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "timezone": "UTC",
            "send_as_reply": True
          },
           {
            "email_number": 2,
            "day": "fri",
            "week": 1,
            "start_time": "10:00:00",
            "end_time": "17:00:00",
            "timezone": "UTC",
            "send_as_reply": True
          }
      ],
      "start_date": LARGE_CAPACITIES[0].send_date,
      "recipients": [12345, 222]
    }
    input =  ScheduleInput.model_validate(data)
    output = Scheduler(service).schedule(input)

    assert(len(output.timetable) == 2)

    recipient_detail = output.timetable[0]
    assert(recipient_detail.recipient_id == 12345)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 2)
    first_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
    first = RecipientSchedule(email_number=1, send_time=first_time)
    second_time = datetime.combine(start_date + timedelta(days=4), time(10, 0, 0))
    second = RecipientSchedule(email_number=2, send_time=second_time)
    assert(recipient_detail.schedule == [first, second])


    recipient_detail = output.timetable[1]
    assert(recipient_detail.recipient_id == 222)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 2)
    first_time = datetime.combine(start_date + timedelta(days=2), time(9, 5, 0))
    first = RecipientSchedule(email_number=1, send_time=first_time)
    second_time = datetime.combine(start_date + timedelta(days=4), time(10, 5, 0))
    second = RecipientSchedule(email_number=2, send_time=second_time)
    assert(recipient_detail.schedule == [first, second])


def test_scheduler_with_three_emails_two_week_campaign():
    service = MagicMock(spec=CampaignService)
    service.calculate_capacity.return_value = LARGE_CAPACITIES
    start_date = LARGE_CAPACITIES[0].send_date
    data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
            "email_number": 1,
            "day": "wed",
            "week": 1,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "timezone": "UTC",
            "send_as_reply": True
          },
           {
            "email_number": 2,
            "day": "fri",
            "week": 1,
            "start_time": "10:00:00",
            "end_time": "17:00:00",
            "timezone": "UTC",
            "send_as_reply": True
          },
          {
            "email_number": 3,
            "day": "fri",
            "week": 2,
            "start_time": "10:00:00",
            "end_time": "17:00:00",
            "timezone": "UTC",
            "send_as_reply": True
          },
      ],
      "start_date": LARGE_CAPACITIES[0].send_date,
      "recipients": [12345, 222]
    }
    input =  ScheduleInput.model_validate(data)
    output = Scheduler(service).schedule(input)

    assert(len(output.timetable) == 2)

    recipient_detail = output.timetable[0]
    assert(recipient_detail.recipient_id == 12345)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 3)
    first_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
    first = RecipientSchedule(email_number=1, send_time=first_time)
    second_time = datetime.combine(start_date + timedelta(days=4), time(10, 0, 0))
    second = RecipientSchedule(email_number=2, send_time=second_time)
    third_time = datetime.combine(start_date + timedelta(days=7 + 4), time(10, 0, 0))
    third = RecipientSchedule(email_number=3, send_time=third_time)
    assert(recipient_detail.schedule == [first, second, third])



    recipient_detail = output.timetable[1]
    assert(recipient_detail.recipient_id == 222)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 3)
    first_time = datetime.combine(start_date + timedelta(days=2), time(9, 5, 0))
    first = RecipientSchedule(email_number=1, send_time=first_time)
    second_time = datetime.combine(start_date + timedelta(days=4), time(10, 5, 0))
    second = RecipientSchedule(email_number=2, send_time=second_time)
    third_time = datetime.combine(start_date + timedelta(days=7 + 4), time(10, 5, 0))
    third = RecipientSchedule(email_number=3, send_time=third_time)
    assert(recipient_detail.schedule == [first, second, third])
    
    def test_scheduler_with_one_email_one_recipient():
      service = MagicMock(spec=CampaignService)
      service.calculate_capacity.return_value = LARGE_CAPACITIES
      start_date = LARGE_CAPACITIES[0].send_date
      data = {
        "campaign_id": 1,
        "sending_account_id": 100,
        "sending_limit": 20 ,
        "schedule": [
            {
            "email_number": 1,
            "day": "wed",
            "week": 1,
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "timezone": "UTC",
            "send_as_reply": True
            }
        ],
        "start_date": start_date,
        "recipients": [12345]
      }
      input =  ScheduleInput.model_validate(data)
      output = Scheduler(service).schedule(input)

      assert(len(output.timetable) == 1)

      recipient_detail = output.timetable[0]
      assert(recipient_detail.recipient_id == 12345)
      assert(recipient_detail.batch_number == 1)
      assert(len(recipient_detail.schedule) == 1)
      schedule_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
      first_schedule = RecipientSchedule(email_number=1, send_time=schedule_time)
      assert(recipient_detail.schedule == [first_schedule])

def test_scheduler_with_older_date():
    service = MagicMock(spec=CampaignService)
    service.calculate_capacity.return_value = LARGE_CAPACITIES
    start_date = LARGE_CAPACITIES[0].send_date
    data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
          "email_number": 1,
          "day": "wed",
          "week": 1,
          "start_time": "09:00:00",
          "end_time": "17:00:00",
          "timezone": "UTC",
          "send_as_reply": True
          }
      ],
      "start_date": start_date,
      "recipients": [12345]
    }
    input =  ScheduleInput.model_validate(data)
    output = Scheduler(service).schedule(input)

    assert(len(output.timetable) == 1)

    recipient_detail = output.timetable[0]
    assert(recipient_detail.recipient_id == 12345)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 1)
    schedule_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
    first_schedule = RecipientSchedule(email_number=1, send_time=schedule_time)
    assert(recipient_detail.schedule == [first_schedule])
    assert output.start_date >= date.today(), "The passed date was older then the current date"
  
def test_scheduler_for_a_passed_time():
    service = MagicMock(spec=CampaignService)
    service.calculate_capacity.return_value = LARGE_CAPACITIES
    start_date = LARGE_CAPACITIES[0].send_date
    data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
          "email_number": 1,
          "day": "wed",
          "week": 1,
          "start_time": "12:00:00",
          "end_time": "17:00:00",
          "timezone": "UTC",
          "send_as_reply": True
          }
      ],
      "start_date": start_date,
      "recipients": [12345]
    }
    input =  ScheduleInput.model_validate(data)
    output = Scheduler(service).schedule(input)

    assert(len(output.timetable) == 1)

    recipient_detail = output.timetable[0]
    assert(recipient_detail.recipient_id == 12345)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 1)
    schedule_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
    first_schedule = RecipientSchedule(email_number=1, send_time=schedule_time)
    assert(input.schedule[0].end_time) > datetime.now().time(), "The given end time has passed"

def test_scheduler_with_one_email_short_window():
    service = MagicMock(spec=CampaignService)
    service.calculate_capacity.return_value = LARGE_CAPACITIES
    start_date = LARGE_CAPACITIES[0].send_date
    data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
          "email_number": 1,
          "day": "wed",
          "week": 1,
          "start_time": "09:00:00",
          "end_time": "17:00:00",
          "timezone": "UTC",
          "send_as_reply": True
          }
      ],
      "start_date": start_date,
      "recipients": [12345,222,111]
    }
    input =  ScheduleInput.model_validate(data)
    output = Scheduler(service).schedule(input)

    assert(len(output.timetable) == 3)

    recipient_detail = output.timetable[1]
    assert(recipient_detail.recipient_id == 222)
    assert(recipient_detail.batch_number == 1)
    assert(len(recipient_detail.schedule) == 1)
    schedule_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
    first_schedule = RecipientSchedule(email_number=1, send_time=schedule_time)
    assert(recipient_detail.schedule == [first_schedule])
    

def test_scheduler_for_low_capacity():
  service = MagicMock(spec=CampaignService)
  service.calculate_capacity.return_value = LARGE_CAPACITIES
  start_date = LARGE_CAPACITIES[0].send_date
  data = {
      "campaign_id": 1,
      "sending_account_id": 100,
      "sending_limit": 20 ,
      "schedule": [
          {
          "email_number": 1,
          "day": "wed",
          "week": 1,
          "start_time": "09:00:00",
          "end_time": "17:00:00",
          "timezone": "UTC",
          "send_as_reply": True
          }
      ],
      "start_date": start_date,
      "recipients": [12345]
    }
  input =  ScheduleInput.model_validate(data)
  output = Scheduler(service).schedule(input)
  assert(len(output.timetable) == 1)
  recipient_detail = output.timetable[0]
  assert(recipient_detail.recipient_id == 12345)
  assert(recipient_detail.batch_number == 1)
  assert(len(recipient_detail.schedule) == 1)
  schedule_time = datetime.combine(start_date + timedelta(days=2), time(9, 0, 0))
  first_schedule = RecipientSchedule(email_number=1, send_time=schedule_time)
  assert(recipient_detail.schedule == [first_schedule])


def test_scheduler_for_batch2_on_the_next_start():
  assert True