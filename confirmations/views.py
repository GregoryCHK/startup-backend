from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Confirmation, ActionPlan, ActionPlanEntry, Accommodation, AccommodationEntry
from .serializers import ConfirmationSerializer, ActionPlanEntrySerializer, ActionPlanSerializer, AccommodationSerializer, AccommodationEntrySerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action

import logging

logger = logging.getLogger(__name__)

class ConfirmationViewSet(viewsets.ModelViewSet): # ViewSet allows crud functions automatically
    queryset = Confirmation.objects.all().order_by('-id')
    serializer_class = ConfirmationSerializer
    # permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation Error: {e.detail}")
            return Response({"error": str(e)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            confirmation_name = instance.name
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # No content in response
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ActionPlanViewSet(viewsets.ModelViewSet):
    queryset = ActionPlan.objects.all()
    serializer_class = ActionPlanSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        confirmation_id = self.request.query_params.get('confirmation_id')
        
        if confirmation_id:
            queryset = queryset.filter(confirmation_id=confirmation_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        confirmation_id = request.data.get('confirmation')
        if ActionPlan.objects.filter(confirmation_id=confirmation_id).exists():
            raise ValidationError({"detail": "Action Plan already exists for this confirmation"})
        
        return super().create(request, *args, **kwargs)
    
    # Custom delete action to delete ActionPlan by confirmationId
    @action(detail=False, methods=["delete"], url_path="by-confirmation/(?P<confirmation_id>[^/.]+)")
    def delete_by_confirmation(self, request, confirmation_id=None):
        try:
            # Get the ActionPlan using the confirmationId (foreign key)
            action_plan = ActionPlan.objects.get(confirmation__id=confirmation_id)
            action_plan.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ActionPlan.DoesNotExist:
            return Response({"detail": "Action plan not found."}, status=status.HTTP_404_NOT_FOUND)
    

class ActionPlanEntryViewSet(viewsets.ModelViewSet):
    queryset = ActionPlanEntry.objects.all()
    serializer_class = ActionPlanEntrySerializer
    permission_classes = [AllowAny]  # Adjust permissions as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        confirmation_id = self.request.query_params.get('confirmation_id')  # Filtering by confirmation_id
        
        if confirmation_id:
            # Filter ActionPlanEntries by the related ActionPlan's Confirmation ID
            queryset = queryset.filter(action_plan__confirmation_id=confirmation_id)
        
        action_plan_id = self.request.query_params.get('action_plan_id')  # Optionally filter by action_plan_id
        
        if action_plan_id:
            queryset = queryset.filter(action_plan_id=action_plan_id)
        
        return queryset.order_by('date', 'time')  # Ordering by date and time
    
    def perform_create(self, serializer):
        action_plan_id = self.request.data.get('action_plan')
        try:
            action_plan = ActionPlan.objects.get(pk=action_plan_id)  # Retrieve ActionPlan by ID
            serializer.save(action_plan=action_plan)  # Save ActionPlanEntry linked to ActionPlan
        except ActionPlan.DoesNotExist:
            raise ValidationError({'action_plan': 'Invalid action plan ID'})  # Error handling if ActionPlan does not exist
        
class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        confirmation_id = self.request.query_params.get('confirmation_id')
        
        if confirmation_id:
            queryset = queryset.filter(confirmation_id=confirmation_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        confirmation_id = request.data.get('confirmation')
        if Accommodation.objects.filter(confirmation_id=confirmation_id).exists():
            raise ValidationError({"detail": "Accommodation Plan already exists for this confirmation"})
        
        return super().create(request, *args, **kwargs)
    
    # Custom delete action to delete ActionPlan by confirmationId
    @action(detail=False, methods=["delete"], url_path="by-confirmation/(?P<confirmation_id>[^/.]+)")
    def delete_by_confirmation(self, request, confirmation_id=None):
        try:
            # Get the ActionPlan using the confirmationId (foreign key)
            accommodation = Accommodation.objects.get(confirmation__id=confirmation_id)
            accommodation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Accommodation.DoesNotExist:
            return Response({"detail": "Accommoadtion plan not found."}, status=status.HTTP_404_NOT_FOUND)
        
class AccommodationEntryViewSet(viewsets.ModelViewSet):
    queryset = AccommodationEntry.objects.all()
    serializer_class = AccommodationEntrySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        accommodation_id = self.request.query_params.get('accommodation_id')
        
        if accommodation_id:
            queryset = queryset.filter(accommodation_id=accommodation_id)
        return queryset.order_by('date', 'time')
    
    def perform_create(self, serializer):
        accommodation_id = self.request.data.get('accommodation')
        try:
            accommodation = Accommodation.objects.get(pk=accommodation_id)
            serializer.save(accommodation=accommodation)
        except Accommodation.DoesNotExist:
            raise ValidationError({'accommodation': 'Invalid accommodation ID'})