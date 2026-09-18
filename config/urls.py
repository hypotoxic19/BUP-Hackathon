# from django.urls import path,include
# urlpatterns=[path('',include('optimizer.urls'))]
from django.urls import path, include


urlpatterns = [

    path(
        '',
        include('optimizer.urls')
    ),

]