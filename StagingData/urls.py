"""StagingData URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GetData import views
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('event/', views.getData,name="event"),
    path('eventBrief/<val>', views.eventBrief,name="eventBrief"),
    url(r'^UserApp/',include("UserApp.urls")),
    path('pythonignite/', views.pythonignite,name="pythonignite"),
    path('search_deviceid_postgres/',views.search_deviceid_postgres,name="search_deviceid_postgres"),
    path('search_deviceid_ignite/',views.search_deviceid_ignite,name="search_deviceid_ignite"),
    url(r'^export_Nielson_csv/csv/$',views.export_Nielson_csv,name="export_Nielson_csv"),
    url(r'^export/csv/$',views.export_users_csv,name="export_users_csv"),
    path('drawgraph/',views.drawgraph,name="drawgraph"),
    url(r'^api/chart/dataRadio',views.CreateChart.as_view()),
    url(r'^api/chart/dataAudio',views.CreateChartAudio.as_view()),
    path('queryresultalter/',views.queryresultalter,name="queryresultalter"),
    path('drawgraphpie/',views.drawgraphpie,name="drawgraphpie"),
    path('drawgraphcohortFM/',views.drawgraphcohortFM,name="drawgraphcohortFM"),
    path('showpyscript/',views.showpyscript,name="showpyscript"),
    path('artistMaster/',views.artistMaster,name="artistMaster"),
    url(r'^exportPaytmRewards/csv/$',views.exportPaytmRewards,name="exportPaytmRewards"),
]
