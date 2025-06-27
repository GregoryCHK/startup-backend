from rest_framework import serializers
from .models import Confirmation, ActionPlanEntry, ActionPlan, Accommodation, AccommodationEntry

class AccommodationEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationEntry
        fields = '__all__'
        read_only_fields = ('id',)

    def validate(self, data):
        accommodation = data['accommodation']
        confirmation = accommodation.confirmation
        if not (confirmation.start_date <= data['check_in'] <= confirmation.end_date):
                raise serializers.ValidationError(
                    "Entry date must be within the confirmation date range"
                )
                
        return data

class AccommodationSerializer(serializers.ModelSerializer):
    accommodation_entries = AccommodationEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Accommodation
        fields = ['id', 'confirmation', 'created_at', 'updated_at', 'accommodation_entries']
        read_only_fields = ('id', 'created_at', 'updated_at')


class ActionPlanEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionPlanEntry
        fields = '__all__'
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Validate that the date is within the confirmation date range.
        """

        # Get the action_plan from data or existing instance (for PATCH)
        action_plan = data.get('action_plan') or getattr(self.instance, 'action_plan', None)
        entry_date = data.get('date') or getattr(self.instance, 'date', None)

        if not action_plan or not entry_date:
            raise serializers.ValidationError("Both action_plan and date are required.")

        # confirmation = action_plan.confirmation

        # if not (confirmation.start_date <= entry_date <= confirmation.end_date):
        #     raise serializers.ValidationError(
        #         "Entry date must be within the confirmation date range."
        #     )

        return data

class ActionPlanSerializer(serializers.ModelSerializer):
    action_plan_entries = ActionPlanEntrySerializer(many=True, read_only=True)
    
    class Meta:
        model = ActionPlan
        fields = ['id', 'confirmation', 'created_at', 'updated_at', 'action_plan_entries']
        read_only_fields = ('id', 'created_at', 'updated_at')
    

class ConfirmationSerializer(serializers.ModelSerializer):
    action_plan = ActionPlanSerializer(read_only=True)
    accommodation = AccommodationSerializer(read_only=True)

    class Meta:
        model = Confirmation
        fields = '__all__' # Includes all fields

    def validate_pax(self, value):
        """Ensure pax is at least 1"""
        if value < 1:
            raise serializers.ValidationError("Pax must be at least 1.")
        return value

    def validate_deposit(self, value):
        """Ensure deposit is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Deposit amount cannot be negative.")
        return value
    