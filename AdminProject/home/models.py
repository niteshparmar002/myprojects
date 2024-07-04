from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe

# Create your models here.

gender = (('Male', 'Male'),('Female', 'Female'),('Other', 'Other'),)
ftypes = (('Company', 'Company'),('Client', 'Client'),('Professional', 'Professional'))
hour = ((6, 6),(8, 8),(12, 12),(24, 24))
experience = ((1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10),(11, 11),(12, 12),(13, 13),(14, 14),(15, 15),(16, 16),(17, 17),(18, 18),(19, 19),(20, 20),)
status = (("Active","Active"),("Inactive","Inactive"),("Delete","Delete"))
source = (('Website', 'Website'),('Android', 'Android'),('iOS', 'iOS'),('AMP', 'AMP'),('PWA', 'PWA'),('Desktop', 'Desktop'))
doctype = (('Passport','Passport'), ('Aadhaar','Aadhaar'), ('DrivingLicence','DrivingLicence'), ('VoterID','VoterID'), ('PanCard','PanCard'), ('ArmsLicence','ArmsLicence'), ('Other','Other'))
PLATFORM = (('Android', 'Android'),('IOS', 'IOS'), ('Web', 'Web'))
action = (('Open', 'Open'),('Close', 'Close'),('Reopen', 'Reopen'),('Resolve', 'Resolve'),('Transfer', 'Transfer'),('Fake', 'Fake'))
method = [('GET','GET'),('HEAD','HEAD'),('POST','POST'),('PUT','PUT'),('DELETE','DELETE'),('CONNECT','CONNECT'),('OPTIONS','OPTIONS'),('TRACE','TRACE'),('PATCH','PATCH')]
ntype = (
    ('Blog', 'Blog'),
    ('Invite','Invite'),
    ('Connection', 'Connection'),
    ('Document', 'Document'),
    ('Transfer', 'Transfer'),
    ('Alert', 'Alert'),
    ('AlertReply', 'AlertReply'),
    ('Team', 'Team'),
    ('Work', 'Work'),
    ('WorkTeam', 'WorkTeam'),
    ('WorkTask', 'WorkTask'),
    ('Leave', 'Leave'),
    ('Complaint', 'Complaint'),
    ('SocietyComplaint', 'SocietyComplaint'),
    ('Feed', 'Feed'),
    ('InwardStock', 'InwardStock'),
    ('OutwardStock', 'OutwardStock'),
    ('Channel', 'Channel'),
    ('Chat', 'Chat'),
    ('Job', 'Job'),
    ('Application', 'Application'),
    ('Poll', 'Poll'),
    ('SocietyPoll', 'SocietyPoll'),
    ('Enquiry', 'Enquiry'),
)

class BaseModel(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True, editable=False)
	utimestamp = models.DateTimeField(auto_now=True, editable=False)
	track = models.TextField(blank=True, editable=False)
	utrack = models.TextField(blank=True, editable=False)
	locate = models.TextField(blank=True,null=True)
	status = models.CharField(max_length=20, choices=status, default='Active')

	class Meta:
		abstract = True

class Service(BaseModel):
	"""docstring for Service"""
	title = models.CharField(max_length=160)
	words = models.PositiveIntegerField(default=0)
	new_words = models.PositiveIntegerField(default=0)
	keyword = models.CharField(max_length=160)
	meta_title = models.CharField(max_length=160)
	meta_description = models.TextField()
	thumbnail = models.ImageField(upload_to='home/service/thumbnail', blank=True)	
	cover = models.ImageField(upload_to='home/service/cover', blank=True)

	class Meta:
		verbose_name_plural = '01. Services'
	
	def __str__(self):
		return (self.title)

class Shift(BaseModel):
	"""docstring for Shift"""
	title = models.CharField(max_length=160)
	start = models.TimeField()
	end = models.TimeField()

	class Meta:
		verbose_name_plural = '02. Shift'
	
	def __str__(self):
		return (self.title)

class User(AbstractUser, BaseModel):
	referrer = models.ForeignKey("self",verbose_name="Referrer", on_delete=models.PROTECT, blank=True, null=True)
	service = models.ForeignKey(Service, verbose_name="Service", on_delete=models.PROTECT, blank=True, null=True)
	shift = models.ForeignKey(Shift, related_name="user_shift", on_delete=models.PROTECT, null=True, blank=True)
	identifier = models.CharField(max_length=100, null=True, blank=True)
	mobile = models.BigIntegerField(null=True, blank=True)
	phone = models.CharField(verbose_name="Alternate mobile", max_length=10, blank=True)
	gender = models.CharField(max_length=6, choices=gender, default='Male')
	dob = models.DateField(null=True, blank=True)
	father = models.CharField(max_length=160,null=True, blank=True)
	image = models.ImageField(upload_to='user/image/', blank=True, null=True, default="default/st-logo.png")
	cover = models.ImageField(upload_to='user/cover/', blank=True, null=True, default="default/st-cover.png")
	tagline = models.CharField(max_length=80, blank=True)
	about = models.TextField(blank=True)
	city = models.CharField(max_length=30, blank=True)
	zipcode = models.IntegerField(blank=True, null=True)
	locality = models.CharField(max_length=30, blank=True)
	address = models.TextField(blank=True)
	latitude = models.FloatField(blank=True, null=True) 
	longitude = models.FloatField(blank=True, null=True)
	occupation = models.CharField(max_length=100, blank=True)
	experience = models.CharField(max_length=100, null=True,blank=True)
	married = models.BooleanField(default=False)
	exman = models.BooleanField(default=False)
	ex_service = models.CharField(max_length=100, blank=True)
	rating = models.FloatField(default=0)
	hours = models.PositiveIntegerField(choices=hour, default=12)
	hourly = models.IntegerField(blank=True, null=True)
	salary = models.IntegerField(default=10000)
	esi = models.IntegerField(verbose_name="ESI Number",default=0)
	pf = models.IntegerField(verbose_name="PF Number",default=0)
	rawdata = models.TextField(blank=True)
	notification = models.BooleanField(default=True)
	facebook = models.URLField(max_length=100, blank=True)
	twitter = models.URLField(max_length=100, blank=True)
	instagram = models.URLField(max_length=100, blank=True)
	linkedin = models.URLField(max_length=100, blank=True)
	otp = models.IntegerField(default=0)
	source = models.CharField(max_length=10, choices=source, default='Website')
	verified = models.BooleanField(default=False)
	multilogin = models.BooleanField(default=False)
	private = models.BooleanField(default=False, verbose_name="Private Profile")
	lock = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Users'
		verbose_name_plural = '03. Users'
	
	def image_tag(self):
		return mark_safe('<img src="/media/%s" width="200" height="200"/>' % (self.image))
	image_tag.short_description = 'Image'
	image_tag.allow_tags = True

class Gallery(BaseModel):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='galleries')
	title = models.CharField(max_length=160)
	description = models.TextField(null=True, blank=True)
	thumbnail = models.ImageField(upload_to='gallery/thumbnail')
	size = models.FloatField(help_text="Size in mbs",default=0)
	location = models.CharField(max_length=11)
	private = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "04. Gallery"

	def __str__(self):
		return self.title
	
class GalleryImage(BaseModel):
	gallery = models.ForeignKey(Gallery, on_delete=models.PROTECT, related_name="image_gallaries")
	image = models.FileField(upload_to='gallery/image')
	size = models.FloatField(help_text="Size in mbs",default=0)

class Banner(BaseModel):
	title = models.CharField(max_length=160)
	image = models.ImageField(upload_to='banner/')
	link = models.URLField(null=True, blank=True)
	platform = models.CharField(max_length=8, choices=PLATFORM, default='Website')
	location = models.CharField(max_length=160)

	class Meta:
		verbose_name_plural = "05. Banner"

	def __str__(self):
		return self.title

class Connection(BaseModel):
	initiator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='initiator')
	receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='receiver')
	accepted = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)
	follow = models.BooleanField(default=True)
	block = models.BooleanField(default=False)
	note = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = "06. Connection"

	def __str__(self):
		return str(self.initiator)+' - '+str(self.receiver)

class Document(BaseModel):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='doc_user')
	doctype = models.CharField(max_length=20, choices=doctype)
	number = models.CharField(verbose_name="Document Number",max_length=50)
	front = models.ImageField(upload_to='document/')
	back = models.ImageField(upload_to='document/')
	verify = models.BooleanField(default=False)
	validity = models.DateField(null=True, blank=True)

	class Meta:
		verbose_name_plural = "07. Document"

	def __str__(self):
		return str(self.user)
	
class Measurement(BaseModel):
	"""docstring for Measurements"""
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="measurements_user")
	height = models.IntegerField(help_text='Please fill details in CM')
	weight = models.IntegerField(help_text='Please fill details in Kg')
	biceps = models.IntegerField(blank=True, null=True, help_text='Please fill details in Inches')
	chest = models.IntegerField(blank=True, null=True, help_text='Please fill details in Inches')
	waist = models.IntegerField(blank=True, null=True, help_text='Please fill details in Inches')
	shoes = models.IntegerField(blank=True, null=True, help_text='Please fill Shoes Size')
	source = models.CharField(max_length=10, choices=source, default='Website')
	verified = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "08. Measurement"

	def __str__(self):
		return str(self.user)

class PanicAlert(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='panic_user')
	helper = models.ForeignKey(User, on_delete=models.PROTECT, related_name='panic_helper', blank=True, null=True)
	latitude = models.FloatField(blank=True, null=True) 
	longitude = models.FloatField(blank=True, null=True)
	note = models.TextField(blank=True, null=True)
	fire = models.BooleanField(default=False)
	police = models.BooleanField(default=False)
	ambulance = models.BooleanField(default=False)
	fake = models.BooleanField(default=False)
	backup = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	utimestamp = models.DateTimeField(auto_now=True)
	track = models.TextField(blank=True, editable=False)
	utrack = models.TextField(blank=True, editable=False)
	locate = models.TextField(blank=True)
	status = models.CharField(max_length=50, choices=action, default='Open')

	class Meta:
		verbose_name_plural = "09. Panic Alert"

	def __str__(self):
		return str(self.user)
	
class PayMethod(BaseModel):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payment_user')
	bank = models.CharField(max_length=160, verbose_name="Bank Name")
	name = models.CharField(max_length=160, verbose_name="Account Holder Name")
	number = models.PositiveBigIntegerField(verbose_name="Account Number")
	ifsc = models.CharField(max_length=20, verbose_name="IFSC Code")
	upi = models.CharField(max_length=50, verbose_name="UPI ID")
	swift = models.CharField(max_length=20, verbose_name="Swift Code", null=True, blank=True)

	class Meta:
		verbose_name_plural = "10. Payment Method"

	def __str__(self):
		return str(self.name) + " | " + str(self.bank)

class Track(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='track_user',null=True,blank=True)
	url = models.URLField()
	method = models.CharField(max_length=10, choices=method, default='GET')
	source = models.CharField(max_length=10, choices=source, default='Desktop')
	response = models.TextField()
	rqtoken = models.TextField()
	rstoken = models.TextField()

	class Meta:
		verbose_name_plural = "11. Track"

	def __str__(self):
		return str(self.user)

class Notifications(BaseModel):
	user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
	ntype = models.CharField(max_length=50, choices=ntype, default='Blog')
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=200, null=True, blank=True)
	body = models.TextField()
	image = models.URLField()
	read = models.BooleanField(default=False)
	archive = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "12. Notifications"

	def __str__(self):
		return self.title

class Career(BaseModel):
	title = models.CharField(max_length=160)
	min_salary = models.PositiveIntegerField(default=0)
	max_salary = models.PositiveIntegerField(default=0)
	logo = models.ImageField(upload_to='career/logo/', default="default/st-logo.png")
	cover = models.ImageField(upload_to='career/cover/')
	designation = models.CharField(max_length=200)
	experience = models.CharField(max_length=10, choices=experience, default='0')

	class Meta:
		verbose_name_plural = "13. Career"

	def __str__(self):
		return str(self.title)

class Applications(BaseModel):
	career = models.ForeignKey(Career, on_delete=models.PROTECT, related_name='application_career')
	name = models.CharField(max_length=160)
	email = models.EmailField()
	mobile = models.PositiveBigIntegerField()
	letter = models.TextField(verbose_name='Cover Letter')
	resume = models.FileField(upload_to='career/application/',help_text="*only pdf is allowed",validators=[FileExtensionValidator(['pdf'], message='Only PDF is allowed.')])
	experience = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name_plural = "14. Applications"

	def __str__(self):
		return str(self.name)

class Contact(BaseModel):
	name = models.CharField(max_length=160)
	email = models.EmailField()
	mobile = models.PositiveBigIntegerField()
	subject = models.CharField(max_length=250)
	message = models.TextField()

	class Meta:
		verbose_name_plural = "15. Contact Us"

	def __str__(self):
		return str(self.name)

class Faqs(BaseModel):
	ftype = models.CharField(max_length=20, choices=ftypes, default='Professional')
	question = models.CharField(max_length=160)
	answer = models.TextField()

	class Meta:
		verbose_name_plural = "16. Faqs"

	def __str__(self):
		return str(self.type) + ' - ' + str(self.question)

class Feedback(BaseModel):
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='feedback_user')
	rating  = models.FloatField(default=0)
	review = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = "17. Feedback"

	def __str__(self):
		return str(self.user)

class Hello(BaseModel):
	user1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='feedback_user11')
	hy  = models.FloatField(default=0)
	hello = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to='hello')

	class Meta:
		verbose_name_plural = "18. Hello"

	def __str__(self):
		return str(self.user1)
