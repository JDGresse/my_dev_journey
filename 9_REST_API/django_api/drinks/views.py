from django.http import JsonResponse
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from .models import Drinks
from .serializers import DrinksSerializer

@api_view(['GET', "POST"])
def drinks_list(request, format=None):

    if request.method == 'GET':
        # get all the drinks
        drinks = Drinks.objects.all()
        # serialize the data
        serializer = DrinksSerializer(drinks, many=True)
        # return json
        return Response(serializer.data) #, safe=False)
        # when returning an object, error is returned - set safe=False, not needed when returning dictionary

    elif request.method == 'POST':
        serializer = DrinksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, id, format=None):

    try:
        drink_details = Drinks.objects.get(pk=id)
    except Drinks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinksSerializer(drink_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DrinksSerializer(drink_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)