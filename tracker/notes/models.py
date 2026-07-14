from django.db import models
from django.conf import settings
#Importing the user class to take care of user details (no need to rebuild the wheel)

# Create your models here.
class Note(models.Model):
    title=models.CharField(max_length=200)
    content= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    is_done= models.BooleanField(default=False)
    category=models.ForeignKey('Category', on_delete=models.CASCADE,null= True, blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Category (models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name