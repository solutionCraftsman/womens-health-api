from rest_framework.test import APITestCase, APIClient
from ..models import CreateCycleRequest, PeriodCycle
from django.urls import reverse
import json
from rest_framework import status
from datetime import datetime

api_client = APIClient()


class CreateCyclesTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            'last_period_date': "2020-06-20",
            'cycle_average': 25,
            'period_average': 5,
            'start_date': "2020-07-25",
            'end_date': "2021-07-25"
        }

        self.mixed_case_payload = {
            'Last_period_date': "2020-06-20",
            'Cycle_average': 25,
            'Period_average': 5,
            'Start_date': "2020-07-25",
            'end_date': "2021-07-25"
        }

        self.missing_data_payload = {
            'cycle_average': 25,
            'period_average': 5,
            'start_date': "2020-07-25",
            'end_date': "2021-07-25"
        }

        self.empty_value_payload = {
            'Last_period_date': "",
            'cycle_average': 25,
            'period_average': 5,
            'start_date': "2020-07-25",
            'end_date': "2021-07-25"
        }

        self.invalid_data_format_payload = {
            'last_period_date': "202-06-20",
            'cycle_average': 25,
            'period_average': 5,
            'start_date': "202-07-25",
            'end_date': "202-07-25"
        }

        self.negative_cycle_average_payload = {
            'last_period_date': "202-06-20",
            'cycle_average': -1,
            'period_average': 5,
            'start_date': "202-07-25",
            'end_date': "202-07-25"
        }

        self.invalid_cycle_average_payload = {
            'last_period_date': "202-06-20",
            'cycle_average': 32,
            'period_average': 5,
            'start_date': "202-07-25",
            'end_date': "202-07-25"
        }

        self.negative_period_average_payload = {
            'last_period_date': "202-06-20",
            'cycle_average': 25,
            'period_average': -1,
            'start_date': "202-07-25",
            'end_date': "202-07-25"
        }

        self.invalid_period_average_payload = {
            'last_period_date': "202-06-20",
            'cycle_average': 25,
            'period_average': 32,
            'start_date': "202-07-25",
            'end_date': "202-07-25"
        }

    def test_create_cycles_with_valid_data(self):
        response = self.create_cycles(self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(response.data.__contains__('total_created_cycles'))
        self.assertEqual(response.data.get('total_created_cycles'), 8)

        self.assertTrue(response.data.__contains__('create_cycle_request_id'))
        created_cycle_id = response.data.get('create_cycle_request_id')
        created_cycle = CreateCycleRequest.objects.get(pk=created_cycle_id)
        self.assertIsNotNone(created_cycle)

        created_cycles = PeriodCycle.objects.filter(create_cycle_request_id=created_cycle_id)
        self.assertEqual(created_cycles.count(), 8)

    @staticmethod
    def create_cycles(payload):
        response = api_client.post(
            reverse('create-cycles'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        return response

    def test_create_cycles_with_mixed_case_data_still_works(self):
        response = self.create_cycles(self.mixed_case_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(response.data.__contains__('total_created_cycles'))
        self.assertEqual(response.data.get('total_created_cycles'), 8)

        self.assertTrue(response.data.__contains__('create_cycle_request_id'))
        created_cycle_id = response.data.get('create_cycle_request_id')
        created_cycle = CreateCycleRequest.objects.get(pk=created_cycle_id)
        self.assertIsNotNone(created_cycle)

        created_cycles = PeriodCycle.objects.filter(create_cycle_request_id=created_cycle_id)
        self.assertEqual(created_cycles.count(), 8)

    def test_create_cycles_with_missing_data_returns_error(self):
        response = self.create_cycles(self.missing_data_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_create_cycles_with_empty_data_returns_error(self):
        response = self.create_cycles(self.empty_value_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_create_cycles_with_invalid_data_format_returns_error(self):
        response = self.create_cycles(self.invalid_data_format_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_create_cycles_with_negative_cycle_average_returns_error(self):
        response = self.create_cycles(self.negative_cycle_average_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_create_cycles_with_invalid_cycle_average_returns_error(self):
        response = self.create_cycles(self.invalid_cycle_average_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_create_cycles_with_negative_period_average_returns_error(self):
        response = self.create_cycles(self.negative_period_average_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_create_cycles_with_invalid_period_average_returns_error(self):
        response = self.create_cycles(self.invalid_period_average_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))


class CyclesEventTest(APITestCase):

    def setUp(self):
        self.create_cycle_request_payload = {
            'last_period_date': "2020-06-20",
            'cycle_average': 25,
            'period_average': 5,
            'start_date': "2020-07-25",
            'end_date': "2021-07-25"
        }

        response = api_client.post(
            reverse('create-cycles'),
            data=json.dumps(self.create_cycle_request_payload),
            content_type='application/json'
        )

        self.create_cycle_request_id = response.data.get('create_cycle_request_id')
        self.start_date = '2021-06-30'
        self.end_date = '2021-07-05'
        self.period_in_session = '2021-07-04'
        self.ovulation_date = '2021-07-12'
        self.fertility_window = '2021-07-08'
        self.pre_ovulation_window = '2021-07-06'
        self.post_ovulation_window = '2021-07-17'
        self.out_of_range_date = '2022-07-17'
        self.invalid_date = '202-07-17'
        self.empty_data = ''
        self.invalid_id = 'abc'

    def test_get_cycles_event_for_period_start_date(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.start_date)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'period_start_date')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.start_date, '%Y-%m-%d').date())

    @staticmethod
    def get_cycles_event(ccr_id, date):
        response = api_client.get(
            reverse('get-cycle-event'),
            {
                'create_cycle_request_id': ccr_id,
                'date': date
            }
        )
        return response

    def test_get_cycles_event_for_period_end_date(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.end_date)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'period_end_date')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.end_date, '%Y-%m-%d').date())

    def test_get_cycles_event_for_period_in_session(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.period_in_session)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'period_in_session')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.period_in_session, '%Y-%m-%d').date())

    def test_get_cycles_event_for_ovulation_date(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.ovulation_date)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'ovulation_date')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.ovulation_date, '%Y-%m-%d').date())

    def test_get_cycles_event_for_fertility_window(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.fertility_window)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'fertility_window')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.fertility_window, '%Y-%m-%d').date())

    def test_get_cycles_event_for_pre_ovulation_window(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.pre_ovulation_window)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'pre_ovulation_window')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.pre_ovulation_window, '%Y-%m-%d').date())

    def test_get_cycles_event_for_post_ovulation_window(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.post_ovulation_window)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.__contains__('event'))
        self.assertTrue(response.data.__contains__('date'))
        self.assertEqual(response.data.get('event'), 'post_ovulation_window')
        self.assertEqual(response.data.get('date'), datetime.strptime(self.post_ovulation_window, '%Y-%m-%d').date())

    def test_get_cycles_event_with_non_existent_id_returns_not_found(self):
        last_create_cycle_request = CreateCycleRequest.objects.all().last()
        response = self.get_cycles_event(getattr(last_create_cycle_request, 'id') + 1, self.start_date)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.data.__contains__('message'))

    def test_get_cycles_event_with_out_of_range_date_returns_not_found(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.out_of_range_date)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.data.__contains__('message'))

    def test_get_cycles_event_with_invalid_date_returns_error(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.invalid_date)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_get_cycles_event_with_empty_id_returns_error(self):
        response = self.get_cycles_event(self.empty_data, self.start_date)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_get_cycles_event_with_empty_date_returns_error(self):
        response = self.get_cycles_event(self.create_cycle_request_id, self.empty_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))

    def test_get_cycles_event_with_invalid_id_returns_error(self):
        response = self.get_cycles_event(self.invalid_id, self.start_date)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.__contains__('message'))



