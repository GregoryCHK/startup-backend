from django.db import models
from django.core.validators import MinValueValidator

class Confirmation(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('Done', 'Done'),
        ('In Progress', 'In Progress'),
        ('Cancelled', 'Cancelled'),
        ('Postponed', 'Postponed'),
    ]

    # Priority choices
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    channel = models.CharField(max_length=255, blank=True)
    agent = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    contact = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    pax = models.IntegerField(validators=[MinValueValidator(0.0)])
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]) # Only positive numbers (0 or greater) are allowed)
    destinations = models.TextField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class ActionPlan(models.Model):
    confirmation = models.OneToOneField(
        Confirmation, 
        on_delete=models.CASCADE,
        related_name='action_plan'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ActionPlanEntry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Issued', 'Issued'),
        ('No Action', 'No Action'),
        ('Cancelled', 'Cancelled'),
    ]
    
    action_plan = models.ForeignKey(
        ActionPlan,
        on_delete=models.CASCADE,
        related_name='action_plan_entries'
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    service = models.CharField(max_length=255, null=True, blank=True)
    supplier = models.CharField(max_length=255, null=True, blank=True)
    net_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier_comments = models.TextField(blank=True, null=True)
    budget_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['date', 'time']
        indexes = [
            models.Index(fields=['action_plan']),    # index on foreign key for filtering
            models.Index(fields=['date', 'time']),   # composite index for ordering
        ]


class Accommodation(models.Model):
    confirmation = models.OneToOneField(
        Confirmation, 
        on_delete=models.CASCADE,
        related_name='accommodation'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccommodationEntry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Issued', 'Issued'),
        ('Cancelled', 'Cancelled'),
    ]

    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        related_name='accommodation_entries'
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    location = models.CharField(max_length=255)
    check_in = models.DateField()
    check_out = models.DateField()
    nights = models.IntegerField()
    hotel = models.CharField(max_length=255)
    type_of_room = models.CharField(max_length=255)
    net_rate = models.DecimalField(max_digits=10, decimal_places=2)
    cancellation_policy = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)

