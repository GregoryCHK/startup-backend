from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConfirmationViewSet, ActionPlanViewSet, ActionPlanEntryViewSet, AccommodationViewSet, AccommodationEntryViewSet

# Create a router and register all viewsets
router = DefaultRouter()
router.register(r'confirmations', ConfirmationViewSet, basename='confirmation')
router.register(r'action-plans', ActionPlanViewSet, basename='actionplan')
router.register(r'action-plan-entries', ActionPlanEntryViewSet, basename='actionplanentry')
router.register(r'accommodation', AccommodationViewSet, basename='accommodation')
router.register(r'accommodation-entries', AccommodationEntryViewSet, basename='accommodationentry')

# Custom URL patterns (if any)
custom_urlpatterns = [
    # You can add any custom endpoints here if needed
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(custom_urlpatterns)),
]