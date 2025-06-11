from .views import PharmacyItemViewSet, DispensedMedicineViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pharmacy-items', PharmacyItemViewSet)
router.register(r'dispensed-medicines', DispensedMedicineViewSet)
urlpatterns = [path('', include(router.urls))]
