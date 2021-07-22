from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'create-cycle-request', views.CreateCycleRequestViewSet)

urlpatterns = [
    path('create-cycles', views.create_cycles, name='create-cycles'),
    path('cycle-event', views.get_cycle_event, name='get-cycle-event'),
    path('', include(router.urls))
]
