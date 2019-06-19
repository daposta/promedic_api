from django.conf.urls import url
from  .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token


urlpatterns = [
     
    url(r'^states/$', StateList.as_view()),
     url(r'^states/(?P<pk>[0-9]+)/$', StateDetail.as_view()),
    url(r'^local_govts/$', LocalGovernmentList.as_view()),
    url(r'^local_govts/(?P<pk>[0-9]+)/$', LGADetail.as_view()),
    url(r'^local_govt_state/$', LocalGovernmentListFilter.as_view()),
    url(r'^blood_groups/$', BloodGroupList.as_view()),
    url(r'^disabilities/$', DisablityList.as_view()),
     url(r'^disabilities/(?P<pk>[0-9]+)/$', DisabilityDetail.as_view()),
    url(r'^allergies/$', AllergyList.as_view()),
     url(r'^allergies/(?P<pk>[0-9]+)/$', AllergyDetail.as_view()),
    url(r'^genotypes/$', GenotypeList.as_view()),
     url(r'^symptoms/$', SymptomList.as_view()),
     url(r'^diseases/$', DiseaseList.as_view()),
      url(r'^diseases/(?P<pk>[0-9]+)/$', DiseaseDetail.as_view()),
     url(r'^kits/$', KitList.as_view()),
     url(r'^concentrations/$', ConcentrationList.as_view()),
     url(r'^doc_types/$', DocumentTypeList.as_view()),
     url(r'^side_effects/$', DrugSideEffectList.as_view()),
     url(r'^hmos/$', HMOList.as_view()),
      url(r'^hmos/(?P<pk>[0-9]+)/$', HMODetail.as_view()),

     # drug-related urls
     url(r'^drug_brands/$', DrugBrandList.as_view()),
     url(r'^drug_classifications/$', DrugClassificationList.as_view()),
     url(r'^drug_forms/$', DrugFormList.as_view()),
     url(r'^drug_dispense_types/$', DrugDispenseTypeList.as_view()),
     url(r'^drug_indications/$', DrugIndicationList.as_view()),
     url(r'^drug_contraindications/$', DrugContraIndicationList.as_view()),
     url(r'^drugs/$', DrugList.as_view()),
     url(r'^drugs/(?P<pk>[0-9]+)/$', DrugDetail.as_view()),
     url(r'^responders/$', ResponderList.as_view()),
     url(r'^responders/(?P<pk>[0-9]+)/$', ResponderDetail.as_view()),
     url(r'^responder_profile_pic/(?P<pk>[0-9]+)/$', ResponderProfilePicUpdate.as_view()),
     url(r'^responder_docs/(?P<pk>[0-9]+)/$', ResponderDocUpdate.as_view()),

       url(r'^r_docs/$', ResponderDocList.as_view()),
       url(r'^r_docs/(?P<pk>[0-9]+)/$', ResponderDocDetail.as_view()),

      url(r'^newsletters/$', NewsletterList.as_view()),
      url(r'^newsletters/(?P<pk>[0-9]+)/$', NewsletterDetail.as_view()),
      url(r'^newsletter_state/(?P<pk>[0-9]+)/$', NewsletterState.as_view()),


       url(r'^subscribers/$', SubscriberList.as_view()),
       url(r'^subscribers/(?P<pk>[0-9]+)/$', SubscriberDetail.as_view()),

       url(r'^partners/$', PartnersList.as_view()),
        url(r'^partners/(?P<pk>[0-9]+)/$', PartnerDetail.as_view()),

        url(r'^test_centers/$', TestCenterList.as_view()),
         url(r'^test_centers/(?P<pk>[0-9]+)/$', TestCenterDetail.as_view()),
        
     url(r'^genders/$', GenderList.as_view()),

      #clients
      url(r'^clients/$', ClientList.as_view()),
      url(r'^clients/(?P<pk>[0-9]+)/$', ClientDetail.as_view()),
  
    url(r'^users/$', UserList.as_view()),
      url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
  

     url(r'^api-token-auth/', obtain_jwt_token),
     url(r'^api-token-refresh/', refresh_jwt_token),
     url(r'^logout/', LogoutView.as_view()),
     

]
urlpatterns = format_suffix_patterns(urlpatterns)
