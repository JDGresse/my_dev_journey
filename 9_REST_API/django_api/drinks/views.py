from django.http import JsonResponse
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework.decorators import api_view
from .models import Drinks
from .serializers import DrinksSerializer

@api_view(['GET', "POST"])
def drinks_list(request):
    
    if request.method == 'GET':
        # get all the drinks
        drinks = Drinks.objects.all()
        # serialize the data
        serializer = DrinksSerializer(drinks, many=True)
        # return json
        return JsonResponse({'drinks': serializer.data}) #, safe=False)
        # when returning an object, error is returned - set safe=False, not needed when returning dictionary

    if request.method == 'POST':
        serializer = DrinksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)