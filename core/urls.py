from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [

#router.register('', )
router.register('local_govts', views.LocalGovernmentViewSet),
router.register('states', views.StateViewSet),
router.register('local_govts', views.LocalGovernmentViewSet),
router.register('area_of_con', views.AreaOfConcentrationViewSet),
router.register('equipment', views.EquipmentViewSet),
router.register('gender', views.GenderViewSet),
router.register('blood_group', views.BloodGroupViewSet),
router.register('blood_type', views.BloodTypeViewSet),
router.register('allergy', views.AllergyViewSet),
router.register('subscriptionType', views.SubscriptionTypeViewSet),
router.register('drugclassification', views.DrugClassificationViewSet),
router.register('drugbrand', views.DrugBrandViewSet),
router.register('drugform', views.DrugFormViewSets),
router.register('drugSideEffect', views.DrugSideEffectViewSet),
router.register('drugindication', views.DrugIndicationViewSets),
router.register('drugcontraindication', views.DrugContraIndicationViewSet),
router.register('drug', views.DrugViewSet),
router.register('symptom', views.SymptomViewsets),
router.register('disablity', views.DisablityViewsets),
router.register('disease', views.DiseaseViewsets),
router.register('users', views.UserViewsets),
#router.register('rest-auth/', include('rest_auth.urls')),
router.register('kits', views.KitViewsets),
]

urlpatterns = router.urls






















