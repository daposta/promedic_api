from django.conf.urls import url
from  .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token


urlpatterns = [
     
   url(r'^register/$', CreateUserView.as_view()),
   url(r'^create_profile/$', CreateProfileView.as_view()),
   # url(r'^profile_detail/$', ClientProfileDetail.as_view()),
    url(r'^current_profile/?$', CurrentProfile.as_view()),
   url(r'^blood_groups/$', BloodGroupList.as_view()),
    url(r'^disabilities/$', DisablityList.as_view()),
    url(r'^allergies/$', AllergyList.as_view()),
    url(r'^genotypes/$', GenotypeList.as_view()),
    url(r'^diseases/$', DiseaseList.as_view()),
    url(r'^genders/$', GenderList.as_view()),
    url(r'^hmos/$', HMOList.as_view()),
     
    url(r'^api-token-auth/', obtain_jwt_token), 

    url(r'^logout/', LogoutView.as_view()),
    url(r'^forgot_password/', ForgotPassword.as_view()),
    url(r'^reset_password/', ResetPassword.as_view()),
    url(r'^activate_user/', ActivateUser.as_view()),
   url(r'^newsletter_unsubscribe/', NewsletterUnsubscribeView.as_view()),
     

]
urlpatterns = format_suffix_patterns(urlpatterns)
