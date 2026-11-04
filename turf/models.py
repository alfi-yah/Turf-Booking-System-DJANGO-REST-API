from django.db import models

# Create your models here.
class TurfDb(models.Model):
	turf_name = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	contact = models.CharField(max_length=15)
	sport_type = models.CharField(max_length=100)
	price_per_hour = models.PositiveIntegerField()
	capacity = models.IntegerField()
	opening_time = models.TimeField()
	closing_time = models.TimeField()	
	available = models.BooleanField(default=True)

	def __str__(self):
		return self.turf_name

class BookingDb(models.Model):
	customer_name = models.CharField(max_length=200)
	phone = models.CharField(max_length=15)
	turf_id = models.IntegerField()
	booking_date = models.DateField()
	booking_time = models.TimeField()
	duration = models.PositiveIntegerField()
	total_amount = models.DecimalField(editable=False, max_digits=10, decimal_places=2)
	status = models.CharField(max_length=25, default="Pending")
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.customer_name