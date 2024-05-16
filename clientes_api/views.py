from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer

import json


@api_view(['GET'])
def get_users(request):

    if(request.method == 'GET'):
        user = User.objects.all()

        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_by_id(request, id):

    try:
        user_id = User.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):
        serializer = UserSerializer(user_id)

    return Response(serializer.data)


@api_view(['GET'])
def bank_manager(request):
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_manager(request):

    #--- GET /api/data/?id=2
    if(request.method == 'GET'):
        try:
            if(request.GET['user_id']):
                user_id = request.GET['user_id']
                try:
                    user = User.objects.get(pk=user_id)
                    
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #--- POST /api/data/ + JSON
    if(request.method == 'POST'):
        
        new_user = request.data
        
        serializer = UserSerializer(data=new_user)

        if(serializer.is_valid()):

            if(User.objects.filter(user_nickname=request.data['user_nickname'])):
                return Response(status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


        return Response(status=status.HTTP_400_BAD_REQUEST)

    #--- PUT /api/data + JSON
    if(request.method == 'PUT'):
        user_id = request.data['user_id']

        try:
            up_user = User.objects.get(pk=user_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(up_user, data=request.data)

        if(serializer.is_valid()):

            if(User.objects.filter(user_nickname=request.data['user_nickname'])):
                return Response(status=status.HTTP_409_CONFLICT)

            serializer.save()
            return Response(status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


    if(request.method == 'DELETE'):
        try:
            user_del = User.objects.get(pk=request.data['user_id'])
            user_del.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

