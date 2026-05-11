from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from trippyapi.models import Trip, TripUser, Attraction, TripAttraction
from .attraction import AttractionSerializer
from django.contrib.auth.models import User


class Trips(ViewSet):
    """Trip view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        trip = Trip()
        trip.name = request.data["name"]
        trip.destination = request.data["destination"]
        trip.country = request.data["country"]
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
            trip.name = request.data["name"]
            trip.destination = request.data["destination"]
            trip.country = request.data["country"]
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

    @action(detail=True, methods=["post", "delete"], url_path="attendee")
    def trip_attendee(self, request, pk=None):

        if request.method == "POST":
            trip = Trip.objects.get(pk=pk)
            if request.auth.user_id == trip.creator_id:
                try:
                    attendee = User.objects.get(username=request.data["username"])
                except User.DoesNotExist:
                    return Response(
                        "User does not exist", status=status.HTTP_404_NOT_FOUND
                    )

                isAdmin = True if attendee.id == trip.creator_id else False

                try:
                    trip_user = TripUser.objects.get(user=attendee, trip=trip)
                    return Response(
                        "User already attending this trip",
                        status=status.HTTP_200_OK,
                    )
                except TripUser.DoesNotExist:
                    pass

                trip_user = TripUser()
                trip_user.user = attendee
                trip_user.trip = trip
                trip_user.isAdmin = isAdmin
                trip_user.save()

                return Response(None, status=status.HTTP_201_CREATED)

            else:
                return Response("No permissions", status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            user = User.objects.get(username=request.data["username"])
            trip = Trip.objects.get(pk=pk)

            try:
                attendee = TripUser.objects.get(user=user, trip=trip)
            except:
                return Response(
                    "Trip User does not exist", status=status.HTTP_404_NOT_FOUND
                )
            if (
                attendee.user_id == request.auth.user_id
                or trip.creator == request.auth.user
            ):
                attendee.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    "No permission to delete user from trip",
                    status=status.HTTP_405_METHOD_NOT_ALLOWED,
                )

    @action(detail=True, methods=["post", "delete"], url_path="attraction")
    def trip_attraction(self, request, pk=None):
        trip = Trip.objects.get(pk=pk)
        user = request.auth.user_id

        try:
            attraction = Attraction.objects.get(id=request.data["id"])
        except Attraction.DoesNotExist:
            return Response(
                "Attraction does not exist", status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "POST" and TripUser.objects.filter(user_id=user).exists():
            try:
                trip_attr = TripAttraction.objects.get(trip=trip, attraction=attraction)
                return Response(
                    "Attraction already added to this trip",
                    status=status.HTTP_200_OK,
                )
            except TripAttraction.DoesNotExist:
                pass
            trip_attr = TripAttraction()
            trip_attr.user_id = user
            trip_attr.trip_id = trip.id
            trip_attr.attraction_id = attraction.id
            trip_attr.save()

            return Response(None, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            try:
                trip_attr = TripAttraction.objects.get(trip=trip, attraction=attraction)
            except:
                return Response(
                    "Trip Attraction does not exist", status=status.HTTP_404_NOT_FOUND
                )
            if (
                user == request.auth.user_id
                or trip.creator == request.auth.user
            ):
                trip_attr.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)


class TripAttractionSerializer(serializers.ModelSerializer):
    attraction = AttractionSerializer()

    class Meta:
        model = TripAttraction
        fields = ("id", "attraction", "user")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username")
        depth = 1


class TripUserSerializer(serializers.ModelSerializer):
    """JSON serializer for Trip users"""

    user = UserSerializer()

    class Meta:
        model = TripUser
        fields = ("id", "user")


class TripSerializer(serializers.ModelSerializer):
    """JSON serializer for Trips"""

    attendees = serializers.SerializerMethodField()
    attractions = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = (
            "id",
            "name",
            "destination",
            "country",
            "departure_date",
            "return_date",
            "imageurl",
            "creator",
            "attendees",
            "attractions",
        )

    def get_attendees(self, obj):
        list = TripUser.objects.filter(trip_id=obj.id)
        return TripUserSerializer(list, many=True).data

    def get_attractions(self, obj):
        list = TripAttraction.objects.filter(trip_id=obj.id)
        return TripAttractionSerializer(list, many=True).data
