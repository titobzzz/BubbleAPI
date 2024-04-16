from django.db import models
import uuid
from users.models import BaseUserProfile
from bubblebackend import settings
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete




class Job(models.Model):
    '''
    A job listing with all its details 
    '''
    CURRENCIES = (
        ("ETH", "Etherum"),
        ("USD", "US Dollar"),
        ("BTC", "Bitcoin"),
        ("SOL","Solana"),
    )
    STATUS = (
        ("open", "Open"),
        ("filled", "Filled"),
        ("unavailable", "Unavailable"),
    ) 
    ROLE_TYPE = (
        ("remote", "Remote"),
        ("permanent", "Permanent"),
        ("contract", "Contract"),
        ("hybrid", "Hybrid"),
        ("full-time", "Full Time"),
        ("internship", "Internship"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, null=False, blank=False)
    listed_by = models.ForeignKey(
        BaseUserProfile,  on_delete=models.CASCADE, related_name='listed_jobs')

    # Job description
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField()
    location = models.CharField(max_length=250, null=False, blank=False)
    fixed_payment = models.BooleanField(default=False)
    pay = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    pay_currency = models.CharField(
        max_length=10, choices=CURRENCIES, default="USD")
    status = models.CharField(max_length=15, choices=STATUS, default="Open")
    role_type = models.CharField(
        max_length=10, choices=ROLE_TYPE, default="Permanent")

    # Metrics
    # liked_by = models.ManyToManyField('users.User', blank=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return f"{self.title} is {self.status}"


class JobProposals(models.Model):
    '''
    Represents a job application for a specific job listing
    '''
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ) 

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_applications')
    applicant = models.ForeignKey(BaseUserProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return f"{self.applicant.first_name} applying for {self.job.title}"





