from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SuperSerializer
from .models import Super


@api_view(['GET', 'POST'])
def supers_list(request):
    
    if request.method == 'GET':

        super_type_param = request.query_params.get('type')
        supers = Super.objects.all()

        if super_type_param:
            supers = supers.filter(super_type__type=super_type_param)
            serializer = SuperSerializer(supers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            custom_dictionary = {
                'heroes' : [],
                'villains' : []
            }
            
            heroes = supers.filter(super_type_id=1)
            villains = supers.filter(super_type__id=2)
            
            hero_serializer = SuperSerializer(heroes, many=True)
            villain_serializer = SuperSerializer(villains, many=True)

            custom_dictionary['heroes'] = hero_serializer.data
            custom_dictionary['villains'] = villain_serializer.data

            return Response(custom_dictionary, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer =  SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    supers = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':
        serializer = SuperSerializer(supers)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = SuperSerializer(supers, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        supers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)