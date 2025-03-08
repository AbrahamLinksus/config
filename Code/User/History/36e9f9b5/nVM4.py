from app.contracts import ScheduleInput, ScheduleOutput, RecipientDetail, RecipientSchedule

class Scheduler:
    def __init__(self, service):
        self.service = service

    def schedule(self, input: ScheduleInput) -> ScheduleOutput:
        return input.calculate_timetable(self.service)