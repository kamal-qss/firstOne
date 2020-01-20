from django.conf.urls import url
from UserApp import views
from django.urls import path
from GetData import views

app_name = 'GetData'

urlpatterns = [
    path('search_deviceid/',views.search_deviceid,name="search_deviceid"),
]