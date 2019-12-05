from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class QR_Code(models.Model):
    owner  = models.ForeignKey(User,on_delete=models.CASCADE)
    device = models.CharField(max_length=100)



    class Meta:
        unique_together = ['owner','device']

    def __str__(self):
        return self.device

    def get_absolute_url(self):
        return reverse('code-detail',kwargs={'pk':self.pk})
    


    
