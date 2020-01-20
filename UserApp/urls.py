from django.conf.urls import url
from UserApp import views
from django.urls import path

app_name = 'UserApp'

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.activate, name='activate'),
    path('signup/',views.signup,name="signup"),
	path('userlogin/',views.userlogin,name="userlogin"),
	path('userHome/',views.userHome,name="userHome"),
	path('passwordreset/',views.passwordreset,name="passwordreset"),
	path('userlogout/',views.userLogout,name="userLogout"),
	path('activateOnRequest/',views.activateOnRequest,name="activateOnRequest"),
	url(r'^api/chart/dataHomePage',views.CreateChartHomePage.as_view()),
	url(r'^api/chart/dataHomeInstallData',views.CreatedataHomePageInstallData.as_view()),
]
