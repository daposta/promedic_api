from django.conf.urls import url
from  .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token


urlpatterns = [
     
    url(r'^dashboard_data/$', DashboardData_ListView.as_view()),
    url(r'^medic_request/$', RequestList.as_view()),
     

]
urlpatterns = format_suffix_patterns(urlpatterns)
