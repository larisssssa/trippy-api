from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from trippyapi.models import Category


class Categories(ViewSet):
    """Category view set"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET requests for all categories

        Returns:
            Response -- JSON serialized array
        """
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Category
        fields = ("id", "name")
