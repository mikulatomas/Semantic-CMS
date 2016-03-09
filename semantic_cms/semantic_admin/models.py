from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from semantic_cms.image_tools import upload_to_id_image, default_quality

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    test_string = models.CharField(max_length=100, blank=True,  null=True)
    bio = models.CharField(max_length=500, blank=True,  null=True)
    profile_image = ProcessedImageField(upload_to=upload_to_id_image,
                                           processors=[ResizeToFill(400, 400)],
                                           format='JPEG',
                                           options={'quality': default_quality}, blank=True, null=True)

    def __str__(self):
        return "User profile"

class BlogSettings(models.Model):
    blog_name = models.CharField(max_length=20, blank=True,  null=True)
    blog_description = models.CharField(max_length=100, blank=True,  null=True)

    def __str__(self):
        return "Basic settings"
