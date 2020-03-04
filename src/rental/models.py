from django.db 		import models
from django.conf 	import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here.
# class Terminal(models.Model):
# 	pass

class Kind(models.Model):
	name 			= models.CharField(max_length=20,primary_key=True,
						validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Name does not allow special charecters',
									),
								])
	title 			= models.CharField(max_length=50,blank=True, null=True,)
	trans_time 		= models.FloatField(verbose_name='AVG transportation time(minutes/day)',default=10)
	handling_time 	= models.FloatField(verbose_name='AVG handling time(minutes/box)',default=2)
	created		 	= models.DateTimeField(auto_now_add=True)
	modified		= models.DateTimeField(auto_now=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,
						blank=True,null=True)
	
	def __str__(self):
		return ('%s' % (self.name))

	def get_absolute_url(self):
		return reverse('rental:kind-detail', kwargs={'pk': self.pk})

class Che(models.Model):
	name 			= models.CharField(max_length=20,primary_key=True,
					validators=[
									RegexValidator(
										regex='^[\w-]+$',
										message='Name does not allow special charecters',
									),
								])
	title 			= models.CharField(max_length=50,blank=True, null=True)
	kind 			= models.ForeignKey(Kind,
							on_delete=models.SET_NULL,
							blank=True, null=True,
							related_name='ches')
	created		 	= models.DateTimeField(auto_now_add=True)
	modified		= models.DateTimeField(auto_now=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,
						blank=True,null=True)
	
	def __str__(self):
		return ('%s' % (self.name))

	def get_absolute_url(self):
		return reverse('rental:che-detail', kwargs={'pk': self.pk})

class Rental(models.Model):
	terminal 		= models.CharField(verbose_name='Terminal',
									max_length=10)
	che 			= models.ForeignKey(Che,
							on_delete=models.SET_NULL,
							blank=True, null=True,
							related_name='rental')
	container 		= models.CharField(verbose_name='Container number',max_length=15)
	rent_date		= models.DateTimeField()
	created		 	= models.DateTimeField(auto_now_add=True)
	modified		= models.DateTimeField(auto_now=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,
						blank=True,null=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return ('%s on %s' % (self.che,self.terminal))

	def get_absolute_url(self):
		return reverse('rental:detail', kwargs={'pk': self.pk})