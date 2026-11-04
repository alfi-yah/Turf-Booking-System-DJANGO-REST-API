from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from turf.models import TurfDb, BookingDb
from turf.serializers import Turf_Serializer, Booking_Serializer
from datetime import time, datetime, timedelta  

# Create your views here.

class TurfListCreateView(APIView):
    def get(self, request):
        qs = TurfDb.objects.all()
        serializer_instance = Turf_Serializer(qs, many=True)
        return Response(data=serializer_instance.data)

    def post(self, request):
        form_data = request.data
        serializer_instance = Turf_Serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TurfRetriveUpdateDeleteView(APIView):
    def get(self, request, pk):
        qs = get_object_or_404(TurfDb, id=pk)
        serializer_instance = Turf_Serializer(qs)
        return Response(data=serializer_instance.data)
    
    def put(self, request, pk):
        form_data = request.data
        turf_object = get_object_or_404(TurfDb, id=pk)
        serializer_instance = Turf_Serializer(data=form_data,instance=turf_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self, request, pk):
        turf_object = get_object_or_404(TurfDb, id=pk)
        turf_object.delete()
        return Response(data={"Message": "Deleted...!"})

class BookingListCreateView(APIView):
    def get(self, request):
        qs = BookingDb.objects.all()
        serializer_instance = Booking_Serializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = Booking_Serializer(data=form_data)

        if serializer_instance.is_valid():

            booking_date = serializer_instance.validated_data.get("booking_date")
            booking_time = serializer_instance.validated_data.get("booking_time")
            duration = serializer_instance.validated_data.get("duration")
            turf_id = serializer_instance.validated_data.get("turf_id")

            turf = get_object_or_404(TurfDb, id=turf_id)

            # Check turf availability
            if turf.available == False:
                return Response(data={
                    "Message": "This turf is currently unavailable."
                })

            # Get opening and closing time
            opening_time = turf.opening_time
            closing_time = turf.closing_time

            # Calculate start and end time
            start_time = datetime.combine(booking_date, booking_time)
            end_time = start_time + timedelta(hours=duration)

            # Check opening time
            if booking_time < opening_time:
                return Response(data={
                    "Message": "Turf is not open yet."
                })

            # Check closing time
            if end_time.time() > closing_time:
                return Response(data={
                    "Message": "Booking exceeds turf closing time."
                })

            # Get existing bookings
            existing_bookings = BookingDb.objects.filter(
                booking_date=booking_date,
                turf_id=turf_id,
                status="Confirmed"
            )

            # Check overlapping bookings
            for booking in existing_bookings:

                existing_start = datetime.combine(
                    booking_date, booking.booking_time
                )

                existing_end = existing_start + timedelta(
                    hours=booking.duration
                )

                if start_time < existing_end and end_time > existing_start:
                    return Response(data={
                        "Message": "This time slot is already booked."
                    })

            # Calculate total amount
            total_amount = turf.price_per_hour * duration

            form_data["total_amount"] = total_amount
            form_data["status"] = "Confirmed"

            qs = BookingDb.objects.create(**form_data)


            return Response(data={
                "Message": "Booked Successfully...!",
                "Booking Time": form_data["booking_time"],
                "Booking Status": form_data["status"],
                "Total Amount": form_data["total_amount"]
            })

        else:
            return Response(data=serializer_instance.errors)