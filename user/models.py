from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=255)

    class Meta:
        db_table='users'
        verbose_name='User'
        verbose_name_plural='Users'

    def __str__(self):
        return self.username

class Recovery(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='recoveries'
        verbose_name='Recovery'
        verbose_name_plural='Recoveries'

    def __str__(self):
        return self.user.username