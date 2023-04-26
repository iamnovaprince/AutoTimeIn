from django.db import models

# Create your models here.

class Session(models.Model):
    
    email = models.EmailField(verbose_name="Email", max_length=300)
    password = models.CharField(verbose_name="Password", max_length=300)
    token = models.CharField(verbose_name="Token", max_length=300)
    
    def __str__(self):
        return str(self.email);