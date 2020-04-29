from django.db 		import models
from django.conf 	import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Department(models.Model):
	name 				= models.CharField(primary_key=True,
							max_length=50,null = False,
							validators=[
										RegexValidator(
											regex='^[\w-]+$',
											message='Name does not allow special charecters',
										),
									])
	description 	= models.CharField(max_length=50,null = True,blank = True)
	created		 	= models.DateTimeField(auto_now_add=True)
	modified		= models.DateTimeField(auto_now=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,
						blank=True,null=True)

	def __str__(self):
		return ('%s' % (self.name))

class Ssr(models.Model):
	number 			= models.SlugField(unique=True,blank=True, null=True)  
	title 			= models.CharField(max_length=100)
	department 		= models.ForeignKey(Department,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'ssrs')
	note			= models.TextField(blank=True, null=True)
	created		 	= models.DateTimeField(auto_now_add=True)
	modified		= models.DateTimeField(auto_now=True)
	completed 		= models.BooleanField(default=False)
	freeform 		= models.BooleanField(default=False)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,
						blank=True,null=True)
	
	def __str__(self):
		return ('%s' % (self.pk))

	def get_absolute_url(self):
		return reverse('ssr:detail', kwargs={'number': self.number})

	@property
	def total_file(self):
		qty = self.files.count()
		return qty
	total_file.fget.short_description = "Total files"

def create_ssr_number(instance, new_slug=None):
	# import datetime
	from datetime import datetime
	now = datetime.now() # current date and time
	default_slug = '%s-%s' % (instance.department,now.strftime('%y%m%d%H%M%S'))
	slug = slugify(default_slug)
	if new_slug is not None:
		slug = new_slug
	qs = Ssr.objects.filter(number=new_slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.count())
		return create_ssr_number(instance, new_slug=new_slug)
	return slug

def pre_save_ssr_receiver(sender, instance, *args, **kwargs):
	if not instance.number:
		instance.number = create_ssr_number(instance)

# To auto generate ssr number
pre_save.connect(pre_save_ssr_receiver, sender=Ssr)


def content_file_name(instance, filename):
	# return '/'.join(['content', instance.user.username, filename])
	return 'files/ssr/%s/%s/%s' % (instance.ssr.department,instance.ssr.number, filename)

# Support multiple image for each contianer
class Ssrfiles(models.Model):
	ssr				= models.ForeignKey(Ssr,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'files')
	note			= models.CharField(max_length=100,blank=True, null=True)
	file 			= models.FileField(upload_to=content_file_name)
	created		 	= models.DateTimeField(auto_now_add=True)
	modified	 	= models.DateTimeField(blank=True, null=True,auto_now=True)
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL,
						on_delete=models.SET_NULL,
						blank=True,null=True)

	def __str__(self):
		return self.ssr.number

	# def get_image_url(self):
	# 	return self.file.url

	def get_absolute_url(self):
		return reverse('ssr:ssrfiles-detail', kwargs={'pk': self.pk})
