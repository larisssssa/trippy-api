from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from trippyapi.models import Trip


class Trips(ViewSet):
    """Trip view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        trip = Trip()
        trip.destination = request.data["destination"]
        trip.departure_date = request.data["departure_date"]
        trip.return_date = request.data["return_date"]
        trip.imageurl = request.data["imageurl"]
        trip.creator = request.auth.user

        try:
            trip.save()
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized instance
        """
        try:
            trip = Trip.objects.get(pk=pk)
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests, updating Trip

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            trip = Trip.objects.get(pk=pk)
            trip.destination = request.data["destination"]
            trip.departure_date = request.data["departure_date"]
            trip.return_date = request.data["return_date"]
            trip.imageurl = request.data["imageurl"]
            trip.save()
        except Trip.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single trip

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            trip = Trip.objects.get(pk=pk)
            trip.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Trip.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all trips

        Returns:
            Response -- JSON serialized array
        """
        try:
            trips = Trip.objects.all()
            serializer = TripSerializer(trips, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class TripSerializer(serializers.ModelSerializer):
    """JSON serializer for Trips"""

    class Meta:
        model = Trip
        fields = (
            "id",
            "destination",
            "departure_date",
            "return_date",
            "imageurl",
            "creator",
        )
