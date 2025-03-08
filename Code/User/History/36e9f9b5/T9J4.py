from app.contracts import ScheduleInput, ScheduleOutput, RecipientDetail, RecipientSchedule, Check_Date
from datetime import datetime , timedelta

class Scheduler:
    def __init__(self, service):
        self.service = service

    def schedule(self, input: ScheduleInput) -> ScheduleOutput:
        timetable = []
        current_batch = 1
        start_date = input.start_date
        send_pace = 5
        mails_to_send = len(input.schedule)*len(input.recipients)
        for index, recipient_id in enumerate(input.recipients):
            schedule_list = []
            datetime_dummy = datetime(2000,1,1)
            time1 = datetime.combine(datetime_dummy,(input.schedule[0].end_time))
            time2 = datetime.combine(datetime_dummy,(input.schedule[0].start_time))
            time_diff_in_minutes = int((time1 - time2).total_seconds()/60)
            gap_inbetween = int(time_diff_in_minutes / mails_to_send)
            for week_schedule in input.schedule:
                email_number = week_schedule.email_number
                days_delta = (week_schedule.week - 1) * 7 + week_schedule.day_number
                date = start_date + timedelta(days=days_delta)
                date = Date_validator(input_date=date)
                schedule_time = datetime.combine(date, week_schedule.start_time) + timedelta(minutes=5 * index)
                schedule_list.append(RecipientSchedule(email_number=email_number, send_time=schedule_time))
            detail = RecipientDetail(recipient_id=recipient_id, batch_number=current_batch, schedule=schedule_list)
            timetable.append(detail)    
        return ScheduleOutput(**input.model_dump(), timetable=timetable)
    
    