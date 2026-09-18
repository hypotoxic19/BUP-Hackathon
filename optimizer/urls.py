from django.urls import path

from .views import (
    dashboard,
    health,
    optimize_energy
)


urlpatterns = [

    path(
        '',
        dashboard
    ),

    path(
        'health',
        health
    ),

    path(
        'optimize-energy',
        optimize_energy
    ),

]