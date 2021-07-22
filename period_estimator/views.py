from datetime import datetime, timedelta
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CreateCycleRequest, PeriodCycle
from .serializers import CreateCycleSerializer


@api_view(['POST'])
def create_cycles(request):
    """ Method to process request to create cycles """
    data = {}
    for key, value in request.data.items():
        data[key.lower()] = value

    try:
        data = {
            'last_period_date': datetime.strptime(data.get('last_period_date'), '%Y-%m-%d'),
            'cycle_average': int(data.get('cycle_average')),
            'period_average': int(data.get('period_average')),
            'start_date': datetime.strptime(data.get('start_date'), '%Y-%m-%d'),
            'end_date': datetime.strptime(data.get('end_date'), '%Y-%m-%d')
        }
    except TypeError:
        return Response({
            'message': 'Error in request data'
        }, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({
            'message': 'Error in request data'
        }, status=status.HTTP_400_BAD_REQUEST)

    period_average = data.get('period_average')
    cycle_average = data.get('cycle_average')

    try:
        validate_create_cycle(period_average, cycle_average)
    except ValueError:
        return Response({
            'message': 'Error in request data',
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = CreateCycleSerializer(data=data, context={'request': request})

    if serializer.is_valid():
        created_cycle = serializer.save()

        start_date = data['start_date']
        last_period_date = data['last_period_date']
        start_creating_cycles = False

        while last_period_date < data['end_date']:

            if start_date > last_period_date:
                start_creating_cycles = True

            if start_creating_cycles:
                period_cycle = PeriodCycle.objects.create(
                    create_cycle_request=created_cycle,
                    start_date=last_period_date + timedelta(days=cycle_average),
                    end_date=last_period_date + timedelta(days=cycle_average + period_average),
                    ovulation_date=last_period_date + timedelta(days=cycle_average + (cycle_average // 2)),
                    fertility_window_start=last_period_date + timedelta(days=cycle_average + (cycle_average // 2) - 4),
                    fertility_window_end=last_period_date + timedelta(days=cycle_average + (cycle_average // 2) + 4),
                    pre_ovulation_window_start=last_period_date + timedelta(days=cycle_average + period_average + 1),
                    pre_ovulation_window_end=last_period_date + timedelta(
                        days=cycle_average + (cycle_average // 2) - 4 - 1),
                    post_ovulation_window_start=last_period_date + timedelta(
                        days=cycle_average + (cycle_average // 2) + 4 + 1),
                    post_ovulation_window_end=last_period_date + timedelta(days=cycle_average + cycle_average - 1)
                )

                last_period_date = getattr(period_cycle, 'start_date')

            last_period_date = last_period_date + timedelta(days=cycle_average)

        created_cycles = PeriodCycle.objects.filter(create_cycle_request_id=created_cycle.id)

        response = {
            'create_cycle_request_id': created_cycle.id,
            'total_created_cycles': created_cycles.count()
        }

        return Response(response, status=status.HTTP_201_CREATED)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def validate_create_cycle(period_average, cycle_average):
    """ Method to validate request to create cycles """
    if cycle_average < 0 or cycle_average > 31:
        raise ValueError('cycle_average of ' + cycle_average + ' is invalid')

    if period_average < 0 or period_average > 31:
        raise ValueError('period_average of ' + cycle_average + ' is invalid')


@api_view(['GET'])
def get_cycle_event(request):
    """ Method to process request to get cycle event """
    try:
        create_cycle_request_id = int(request.query_params.get('create_cycle_request_id', ''))
        date = datetime.strptime(request.query_params.get('date', ''), '%Y-%m-%d')
    except TypeError:
        return Response({
            'message': 'Error in request parameter',
        }, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({
            'message': 'Error in request parameter',
        }, status=status.HTTP_400_BAD_REQUEST)

    period_cycles = PeriodCycle.objects.filter(create_cycle_request_id=create_cycle_request_id)

    if period_cycles is None:
        return Response({
            'message': 'Request with id ' + str(create_cycle_request_id) + ' not found'
        }, status=status.HTTP_404_NOT_FOUND)

    has_found_event = False
    event: str = ''

    for period_cycle in period_cycles:

        if getattr(period_cycle, 'start_date') == date:
            event = 'period_start_date'
            has_found_event = True
        elif getattr(period_cycle, 'start_date') < date < getattr(period_cycle, 'end_date'):
            event = 'period_in_session'
            has_found_event = True
        elif getattr(period_cycle, 'end_date') == date:
            event = 'period_end_date'
            has_found_event = True
        elif getattr(period_cycle, 'ovulation_date') == date:
            event = 'ovulation_date'
            has_found_event = True
        elif getattr(period_cycle, 'fertility_window_start') <= date <= getattr(period_cycle, 'fertility_window_end'):
            event = 'fertility_window'
            has_found_event = True
        elif getattr(period_cycle, 'pre_ovulation_window_start') <= date <= getattr(period_cycle, 'pre_ovulation_window_end'):
            event = 'pre_ovulation_window'
            has_found_event = True
        elif getattr(period_cycle, 'post_ovulation_window_start') <= date <= getattr(period_cycle, 'post_ovulation_window_end'):
            event = 'post_ovulation_window'
            has_found_event = True

        if has_found_event:
            return Response(
                {
                    'event': event,
                    'date': date.date()
                },
                status=status.HTTP_200_OK
            )

    return Response({
        'message': 'No Event Found for date ' + str(date)
    }, status=status.HTTP_404_NOT_FOUND)


class CreateCycleRequestViewSet(viewsets.ModelViewSet):
    queryset = CreateCycleRequest.objects.all()
    serializer_class = CreateCycleSerializer


