from rest_framework import serializers
from watchlist.models import WatchList,StreamPlatform,Review


        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        exclude=['movie','user',]
        
        
class WatchListSerializer(serializers.ModelSerializer):
    review=ReviewSerializer(many=True,read_only=True)
    class Meta:
        model=WatchList
        fields="__all__"
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist=WatchListSerializer(many=True,read_only=True)
    class Meta:
        model=StreamPlatform   
        fields="__all__"
    
        
# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     description=serializers.CharField(validators=[description1])
#     active=serializers.BooleanField()
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
#     def update(self,instance,validated_data):
#         instance.name=validated_data.get('name',instance.name)
#         instance.description=validated_data.get('description',instance.description)
#         instance.active=validated_data.get('active',instance.active)
#         instance.save()
#         return instance
#     def validate_name(self,value):
#         if(len(value)<2):
#             raise serializers.ValidationError("Name is too short!")
#         else:
#             return value
#     def validate(self,data):
#         if(data['name']==data['description']):
#             raise serializers.ValidationError("Name and descrption should not be same")
        
