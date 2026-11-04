from rest_framework import serializers
from turf.models import TurfDb, BookingDb
from django.utils import timezone

class Turf_Serializer(serializers.ModelSerializer):
	class Meta:
		model = TurfDb
		fields = "__all__"
		read_only_fields = ["id"]

class Booking_Serializer(serializers.ModelSerializer):
	class Meta:
			model = BookingDb
			fields = "__all__"
			read_only_fields = ["id"]
	def validate(self, validated_data):
		booking_date = validated_data.get("booking_date")

        # Prevent booking past dates
		if booking_date < timezone.localdate():
			raise serializers.ValidationError(
                "Past dates are not allowed...!"
            )
		return validated_data