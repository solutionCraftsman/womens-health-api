from django.db import models


class CreateCycleRequest(models.Model):
    last_period_date = models.DateTimeField()
    cycle_average = models.IntegerField()
    period_average = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return str(self.id) + ' ' + str(self.start_date.date()) + ' -> ' + str(self.end_date.date())


class PeriodCycle(models.Model):
    create_cycle_request = models.ForeignKey(CreateCycleRequest, on_delete=models.CASCADE, related_name='create_cycle_request')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ovulation_date = models.DateTimeField()
    fertility_window_start = models.DateTimeField()
    fertility_window_end = models.DateTimeField()
    pre_ovulation_window_start = models.DateTimeField()
    pre_ovulation_window_end = models.DateTimeField()
    post_ovulation_window_start = models.DateTimeField()
    post_ovulation_window_end = models.DateTimeField()
    no_longer_valid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.create_cycle_request.id) + ' ' + str(self.start_date.date()) + ' -> ' + str(self.end_date.date())


