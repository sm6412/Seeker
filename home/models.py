from django.db import models
from django.contrib.auth.models import User

class QR_Code(models.Model):
    owner  = models.ForeignKey(User,on_delete=models.CASCADE)
    device = models.CharField(max_length=100)
    qr_code = models.IntegerField() 

    def __str__(self):
        return self.device
