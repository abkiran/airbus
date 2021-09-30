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


class InventoryDetail(APIView):
    """
    Retrieve, update or delete a Inventory instance.
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    pagination_class = SmallResultsSetPagination

    def get_object(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            inv = Inventory.objects.all()
        else:
            inv = self.get_object(pk)
        serializer = InventorySerializer(inv)
        return Response(inv)

    def put(self, request, pk, format=None):
        inv = self.get_object(pk)
        serializer = InventorySerializer(inv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inv = self.get_object(pk)
        inv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @permission_classes((IsAuthenticated,))
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
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
# @permission_classes((IsAuthenticated,))
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
