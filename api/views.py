from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from myapp.models import Movies,Reviews

from rest_framework.response import Response
from django.contrib.auth.models import User
from api.serlizer import UserSerializer,Movieserializer,Reviewserilizer
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.



class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user==obj.user


class Usersview(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    http_method_names=["post"]

class Moviesview(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    serializer_class=Movieserializer
    queryset=Movies.objects.all()    
    authentication_classes=[authentication.BasicAuthentication]
    # authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kw):
        id=kw.get("pk")
        movie_obj=Movies.objects.get(id=id)
        user=request.user
        serializer=Reviewserilizer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    


class ReviewsView(GenericViewSet,UpdateModelMixin,DestroyModelMixin):
    serializer_class=Reviewserilizer
    queryset=Reviews.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
   # authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    permission_classes=[IsOwner]    

