from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import CustomUser  
import requests
from django.core.files import File
import mimetypes


@receiver(post_save, sender=SocialAccount)
def update_custom_user_with_social_info(sender, instance, created, **kwargs):
    if created:
        # Check if the social account is newly created
        user = instance.user
        custom_user = CustomUser.objects.get(id=user.id)  # Get your custom user instance
        
        # Update custom user model with social information
        custom_user.email = instance.extra_data.get('email', custom_user.email)
        custom_user.full_name = instance.extra_data.get('name', custom_user.full_name)
        
         # Download and save the profile picture
        picture_url = instance.extra_data.get('picture')
        if picture_url:
            response = requests.get(picture_url, stream=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if content_type:
                    extension = mimetypes.guess_extension(content_type)
                    if extension:
                        file_name = f"{user.id}{extension}"
                        custom_user.profile_image.save(file_name, File(response.raw))
        
        custom_user.save()




