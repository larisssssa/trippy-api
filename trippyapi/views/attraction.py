from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from trippyapi.models import Attraction
from .category import CategorySerializer


class Attractions(ViewSet):
    """Attraction view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        attraction = Attraction()
        attraction.name = request.data["name"]
        attraction.description = request.data["description"]
        attraction.imageurl = request.data["imageurl"]
        attraction.category = request.data["category"]

        try:
            attraction.save()
            serializer = AttractionSerializer(attraction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single attraction

        Returns:
            Response -- JSON serialized instance
        """
        try:
            attraction = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(attraction)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests, update Attraction

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            attraction = Attraction.objects.get(pk=pk)
            attraction.name = request.data["name"]
            attraction.description = request.data["description"]
            attraction.imageurl = request.data["imageurl"]
            attraction.category = request.data["category"]
            attraction.save()
        except Attraction.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single attraction

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            attraction = Attraction.objects.get(pk=pk)
            attraction.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Attraction.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all attractions

        Returns:
            Response -- JSON serialized array
        """
        try:
            attractions = Attraction.objects.all()
            serializer = AttractionSerializer(attractions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class AttractionSerializer(serializers.ModelSerializer):
    """JSON serializer for attraction"""

    category = CategorySerializer()

    class Meta:
        model = Attraction
        fields = ("id", "name", "description", "imageurl", "category")
        depth = 1
