from django.http import JsonResponse
from .models import Drinks
from .serializers import DrinksSerializer
from rest_framework.decorators import api_view

@api_view('GET', "POST")
def drinks_list(requst):
    # get all the drinks
    drinks = Drinks.objects.all()
    # serialize the data
    serializer = DrinksSerializer(drinks, many=True)
    # return json
    return JsonResponse({'drinks': serializer.data}) #, safe=False)
    # when returning an object, error is returned - set safe=False, not needed when returning dictionary

