from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Floor, ParkingSpot, ParkingSession, Rate
from datetime import datetime, timezone


class LoginView(APIView):
    def post(self, request):
        license_plate = request.GET.get('license_plate')
        vehicle_type = request.GET.get('vehicle_type')
        floor_data = Floor.objects.all()

        for floor in floor_data:
            spots = ParkingSpot.objects.filter(floor=floor, spot_type=vehicle_type)
            free_spot = spots.filter(is_occupied=False)
            if free_spot:
                free_spot = free_spot.first()
                free_spot_id = free_spot.id
                obj = ParkingSpot.objects.get(id=free_spot_id)
                obj.is_occupied = True
                obj.save()
                session_obj = ParkingSession.objects.create(license_plate=license_plate, parking_spot=obj)
                return Response({'floor': floor.floor_number, 'free_spot_id': free_spot_id, 'session_id': session_obj.id})

        return Response({'message': 'No free spots available'})


class LogoutView(APIView):
    def post(self, request):
        session_id = request.GET.get('session_id')
        session_obj = ParkingSession.objects.get(id=session_id)
        spot_type = session_obj.parking_spot.spot_type
        rate_per_hour = Rate.objects.get(spot_type=spot_type).rate_per_hour
        end_time = datetime.now(timezone.utc)
        total_cost = (end_time - session_obj.start_time).seconds * rate_per_hour / 3600
        session_obj.end_time = end_time
        session_obj.total_cost = total_cost
        session_obj.save()
        parking_spot_obj = session_obj.parking_spot
        parking_spot_obj.is_occupied = False
        parking_spot_obj.save()

        return Response({'message': 'Successfully logged out', 'total_cost': total_cost})


class RateChangeView(APIView):
    def post(self, request):
        spot_type = request.GET.get('spot_type')
        rate_per_hour = request.GET.get('rate_per_hour')
        rate_obj = Rate.objects.get(spot_type=spot_type)
        rate_obj.rate_per_hour = rate_per_hour
        rate_obj.save()

        return Response({'message': 'Rate changed successfully'})


