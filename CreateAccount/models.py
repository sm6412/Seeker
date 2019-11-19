from django.db import models

# Create your models here.
class User(models.Model):
	first_name = models.CharField()
	last_name = models.CharField()
	username = models.CharField()
	password = models.CharField()
	email = models.EmailField()
	phone_number = models.BigIntegerField()

class QR_Code(models.Model):
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	device_name = models.CharField()
	# QR code
