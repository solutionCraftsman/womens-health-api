from django.test import TestCase
from ..models import CreateCycleRequest, PeriodCycle
from datetime import datetime


class CreateCycleRequestTest(TestCase):

    def setUp(self):
        self.create_cycle_request = CreateCycleRequest.objects.create(
            last_period_date=datetime.strptime("2020-06-20", '%Y-%m-%d'),
            cycle_average=25,
            period_average=5,
            start_date=datetime.strptime("2020-07-25", '%Y-%m-%d'),
            end_date=datetime.strptime("2021-07-25", '%Y-%m-%d')
        )

    def test_create_cycle_request(self):
        create_cycle = CreateCycleRequest.objects.get(pk=self.create_cycle_request.id)
        self.assertEqual(create_cycle.last_period_date, datetime.strptime("2020-06-20", '%Y-%m-%d'))
        self.assertEqual(create_cycle.cycle_average, 25)
        self.assertEqual(create_cycle.period_average, 5)
        self.assertEqual(create_cycle.start_date, datetime.strptime("2020-07-25", '%Y-%m-%d'))
        self.assertEqual(create_cycle.end_date, datetime.strptime("2021-07-25", '%Y-%m-%d'))


class PeriodCycleTest(TestCase):

    def setUp(self):
        self.create_cycle_request = CreateCycleRequest.objects.create(
            last_period_date=datetime.strptime("2020-06-20", '%Y-%m-%d'),
            cycle_average=25,
            period_average=5,
            start_date=datetime.strptime("2020-07-25", '%Y-%m-%d'),
            end_date=datetime.strptime("2021-07-25", '%Y-%m-%d')
        )

        self.test_date = datetime.strptime("2021-01-01", '%Y-%m-%d')

        self.period_cycle = PeriodCycle.objects.create(
            create_cycle_request=self.create_cycle_request,
            start_date=self.test_date,
            end_date=self.test_date,
            ovulation_date=self.test_date,
            fertility_window_start=self.test_date,
            fertility_window_end=self.test_date,
            pre_ovulation_window_start=self.test_date,
            pre_ovulation_window_end=self.test_date,
            post_ovulation_window_start=self.test_date,
            post_ovulation_window_end=self.test_date
        )

    def test_period_cycle(self):
        period_cycle = PeriodCycle.objects.get(pk=self.period_cycle.id)
        self.assertEqual(period_cycle.create_cycle_request, self.create_cycle_request)
        self.assertEqual(period_cycle.start_date, self.test_date)
        self.assertEqual(period_cycle.end_date, self.test_date)
        self.assertEqual(period_cycle.ovulation_date, self.test_date)
        self.assertEqual(period_cycle.fertility_window_start, self.test_date)
        self.assertEqual(period_cycle.fertility_window_end, self.test_date)
        self.assertEqual(period_cycle.pre_ovulation_window_start, self.test_date)
        self.assertEqual(period_cycle.pre_ovulation_window_end, self.test_date)
        self.assertEqual(period_cycle.post_ovulation_window_start, self.test_date)
        self.assertEqual(period_cycle.post_ovulation_window_end, self.test_date)
