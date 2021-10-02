from django.http import Http404, JsonResponse, HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from airbus.events import SmallResultsSetPagination
from inventory.models import Inventory
from inventory.serializers import InventorySerializer



@api_view(['GET', 'POST'])
@csrf_exempt
def inventory_list(request):
    """
    List all code inventory, or create a new inventory.
    """
    if request.method == 'GET':
        inventory = Inventory.objects.all()
        # paginator = PageNumberPagination()
        # inventory = paginator.paginate_queryset(inventory, request)
        serializer = InventorySerializer(inventory, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = InventorySerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                print(e)
                return JsonResponse(
                    {
                        "detail": "There is a record exists with the same product id, please try with a different one"
                    }, status=409)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def inventory_detail(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = InventorySerializer(inventory)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = InventorySerializer(inventory, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        inventory.delete()
        return HttpResponse(status=204)
