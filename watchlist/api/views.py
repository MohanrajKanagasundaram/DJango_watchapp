from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from distutils.file_util import move_file
from watchlist.models import WatchList,StreamPlatform,Review
from watchlist.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from watchlist.api.permissions import AdminReadOnly
from watchlist.api.paginations import ReviewPagination,MovieListPagination



class CreateReview(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self,serializer):
        permission_classes=[IsAuthenticated]
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(movie=watchlist,user=review_user)
        if review_queryset.exists():
            raise ValidationError("you have already reviewed this")
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(serializer.validated_data['rating']+watchlist.avg_rating)/2
        watchlist.number_rating=watchlist.number_rating+1
        watchlist.save()
        serializer.save(movie=watchlist,user=review_user)
class ReviewUser(generics.ListAPIView):
    serializer_class=ReviewSerializer
    queryset=Review.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username', 'active']
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'rating']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['user__username', 'rating']
    ordering=['rating']
    # permission_classes=[IsAuthenticated]
    # def get_queryset(self):
    #     pk=self.kwargs['pk']
    #     return Review.objects.filter(user__username=pk)
    # def get_queryset(self):
    #    username=self.request.query_params.get('username',None)
    #    return Review.objects.filter(user__username=username)
class ReviewList(generics.ListAPIView):
    serializer_class=ReviewSerializer
    # permission_classes=[IsAuthenticated]
    pagination_class=ReviewPagination
    queryset=Review.objects.all()
    # def get_queryset(self):
    #     pk=self.kwargs['pk']
    #     return Review.objects.filter(movie=pk)
class ReviewDetail(generics.UpdateAPIView,generics.DestroyAPIView,generics.RetrieveAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer

# class Review_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     permission_classes=[IsAuthenticated]
#     def get(self,request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#     def post(self,request, *args, **kwargs):
#         return self.create(request,*args,**kwargs)
# class Review_detail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#     def put(self,request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    

class WatchList(generics.ListAPIView):
    serializer_class = WatchListSerializer
    queryset=WatchList.objects.all()
    pagination_class=MovieListPagination
    
class WatchListAV(APIView):
    def get(self,request):
        data=WatchList.objects.all()
        Resp=WatchListSerializer(data,many=True,context={'request': request}) #Because it is going to return mult
        return Response(Resp.data)
    def post(self,request):
        serializer=WatchListSerializer(data=request.data)
        if(serializer.is_valid()):
             serializer.save()
             return Response(serializer.data)
        else:
           return  Response(serializer.errors)
class WatchListDetail(APIView):
     def get(self,requeset,pk):
        data=WatchList.objects.get(pk=pk)
        Resp=WatchListSerializer(data)
        return Response(Resp.data)
     def put(self,request,pk):
         movie=WatchList.objects.get(pk=pk)
         serializer=WatchListSerializer(movie,data=request.data)
         if(serializer.is_valid()):
             serializer.save()
             return Response(serializer.data)
         else:
             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
     def delete(self,request,pk):
         data=WatchList.objects.get(pk=pk)
         data.delete()
         return Response(status=status.HTTP_404_NOT_FOUND)
     
class StreamPlatformVS(viewsets.ViewSet):
 
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(user,context={'request': request})
        return Response(serializer.data)
class StreamPlatformDetail(APIView):
     def get(self,requeset,pk):
        data=StreamPlatform.objects.get(pk=pk)
        Resp=StreamPlatformSerializer(data)
        return Response(Resp.data)
     def put(self,request,pk):
         movie=StreamPlatform.objects.get(pk=pk)
         serializer=StreamPlatformSerializer(movie,data=request.data)
         if(serializer.is_valid()):
             serializer.save()
             return Response(serializer.data)
         else:
             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
     def delete(self,request,pk):
         data=StreamPlatform.objects.get(pk=pk)
         data.delete()
         return Response(status=status.HTTP_404_NOT_FOUND)
     
# class Review_list(APIView):
#     def get(self,request):
#         data=Review.objects.all()
#         Resp=ReviewSerializer(data,many=True)
#         return Response(Resp.data)
#     def post(self,request):
        
#         Resp=ReviewSerializer(data=request.data)
#         if(Resp.is_valid()):
#             Resp.save()
#             return Response(Resp.data)
#         else:
#             return Response(Resp.errors)
# class Review_detail(APIView):
#     def get(self,request,pk):
#         data=Review.objects.get(pk=pk)
#         Resp=ReviewSerializer(data)
#         return Response(Resp.data)
    
#     def put(self,request,pk):
#         review=Review.objects.get(pk=pk)
#         Resp=ReviewSerializer(review,data=request.data)
#         if(Resp.is_valid()):
#             Resp.save()
#             return Response(Resp.data)
#         else:
#             return Response(Resp.errors)
        
#     def delete(self,request,pk):
#         data=Review.objects.get(pk=pk)
#         data.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)  
        
# @api_view(['GET','POST'])
# def movie_list(request):
#     if(request.method=='GET'):
#         data=Movie.objects.all()
#         Resp=MovieSerializer(data,many=True) #Because it is going to return mult
#         return Response(Resp.data)
#     elif(request.method=='POST'):
#         serializer=MovieSerializer(data=request.data)
#         if(serializer.is_valid()):
#              serializer.save()
#              return Response(serializer.data)
#         else:
#            return  Response(serializer.errors)
             
# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request,pk):
#      if(request.method=='GET'):
#         data=Movie.objects.get(pk=pk)
#         Resp=MovieSerializer(data)
#         return Response(Resp.data)
#      elif(request.method=='PUT'):
#          movie=Movie.objects.get(pk=pk)
#          serializer=MovieSerializer(movie,data=request.data)
#          if(serializer.is_valid()):
#              serializer.save()
#              return Response(serializer.data)
#          else:
#              return Responszze(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#      else:
#          data=Movie.objects.get(pk=pk)
#          data.delete()
         
             
        
        