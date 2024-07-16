from django.shortcuts import render
from rest_framework import status 
from .Serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

# class ListTodo(generics.ListAPIView):
#     queryset = ToDo.objects.all()
#     serializer_class = TodoSerializer

# class DetailTodo(generics.ListAPIView):
#     queryset=ToDo.objects.all()
#     serializer_class = TodoSerializer
    
# class createTodo(generics.CreateAPIView):
#     queryset = ToDo.objects.all()
#     serializer_class = TodoSerializer

# class DeleteTodo(generics.DestroyAPIView):
#     queryset = ToDo.objects.all()
#     serializer_class=TodoSerializer

class TaskListview(APIView):
    def get(self, request,pk=None):
        if pk :
            try:
                task = ToDo.objects.get(id=pk)
                serializer = TodoSerializer(task,many=False)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except :
                return Response(serializer.errors)
        else:
            try:
                task = ToDo.objects.all()
                serializer = TodoSerializer(task,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
            

    def post(self,requst):
        try:
            serializer = TodoSerializer(data=requst.data)
            if serializer.is_valid() :
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.data,status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(serializer.data,status=status.HTTP_404_NOT_FOUND)
        

    def patch(self,request,pk=None):
        if pk:
            try:
                task = ToDo.objects.get(id=pk)
                serializer = TodoSerializer(task,many=False,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                return Response(serializer.data,status=status.HTTP_404_NOT_FOUND)
            

    def delete (self,request,pk):
        try:
            task = ToDo.objects.get(id=pk)
            serializer = TodoSerializer(task,many=False)
            task.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
            




