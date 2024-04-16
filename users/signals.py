from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
# from wta_api_build import settings
from django.utils.encoding import smart_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
# from bubblebackend.settings import DEFAULT_FROM_EMAIL, DOMAIN
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import get_template

from users.models import *

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    '''
    Creates a company profile for every user created, if said user is_organisation.
    If not, creates a BaseUserProfile for it
    '''
    if created:
       
        try:
            base_profile = BaseUserProfile.objects.get(user=instance)
            #print("Base user profile already exists")
        except BaseUserProfile.DoesNotExist:
            try:
                # If the profile does not exist, create a new one
                base_profile = BaseUserProfile.objects.create(user=instance)
                #print("Base user profile created")
            except Exception as e:
                print(f"Error creating Base user profile: {e}")

        # Check and create specific profiles based on flags
       



@receiver(post_save, sender=get_user_model())
def send_email_confirmation_email(sender, instance, created, **kwargs):
    if created:
#         try:
#             subject = 'Confirm Your Email Address'
#             context = {
#                 'first_name': instance.email,
#                 'domain': DOMAIN,

#                 'uid': urlsafe_base64_encode(smart_bytes(instance.pk)),
#                 'token': default_token_generator.make_token(instance),    
#                 }
#             #message = f"http://{context['domain']}/accounts/confirm-email/{context['uid']}/{context['token']}/"
#             template = get_template('email-confirmation.html').render(context)
#             from_email = DEFAULT_FROM_EMAIL
#             to_email = instance.email
            
#             print('Sending email.... ')
# #message,
#             send_mail(
#                 subject, 
#                 None,
#                 from_email, 
#                 [to_email], 
#                 html_message = template,
#                 fail_silently=False
#             )
            
            print('Email sent 👍')
        # except Exception as e:
        #     print(f'Error sending confirmation email: {e}')
        
