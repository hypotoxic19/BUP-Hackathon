from django.urls import path
from .views import health,optimize_energy
urlpatterns=[
path('health',health),
path('optimize-energy',optimize_energy)
]