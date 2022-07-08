from django.db import models
class users(models.Model):
	username=models.CharField(max_length=50)
	password=models.CharField(max_length=50)
	preference=models.CharField(max_length=200,default='none')
	history=models.CharField(max_length=200, default='none')
	notifications=models.CharField(max_length=200,default='none')
	image_url=models.CharField(max_length=300,default='https://imgs.search.brave.com/Wmgf1m-wbgzOgdfoZcSGBb5C7baYyA-_V99Okq6dyro/rs:fit:256:225:1/g:ce/aHR0cHM6Ly90c2U0/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC5m/TWVtTUdKTklQZDVm/TFRJNlR3SndRSGFI/YSZwaWQ9QXBp')

class comments(models.Model):
	auther=models.CharField(max_length=50)
	Text=models.CharField(max_length=1000)
	child=models.CharField(max_length=60)
	parent=models.IntegerField(default=0)
	image_url=models.CharField(max_length=300,default='https://imgs.search.brave.com/Wmgf1m-wbgzOgdfoZcSGBb5C7baYyA-_V99Okq6dyro/rs:fit:256:225:1/g:ce/aHR0cHM6Ly90c2U0/Lm1tLmJpbmcubmV0/L3RoP2lkPU9JUC5m/TWVtTUdKTklQZDVm/TFRJNlR3SndRSGFI/YSZwaWQ9QXBp')
	

class tags(models.Model):
	Text=models.CharField(max_length=100)
	child=models.CharField(max_length=200, default='none')
class hash_data(models.Model):
	Text=models.CharField(max_length=100)
	child=models.CharField(max_length=200)






