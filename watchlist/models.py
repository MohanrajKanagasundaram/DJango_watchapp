from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class StreamPlatform(models.Model):
    name=models.CharField(max_length=30)
    about=models.CharField(max_length=100)
    website=models.URLField(max_length=30)
    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title=models.CharField(max_length=50)
    avg_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    stroyline=models.CharField(max_length=100)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,related_name="watchlist",default=None)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
class Review(models.Model):
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=200)
    movie=models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name='review')
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True,null=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.rating)
    