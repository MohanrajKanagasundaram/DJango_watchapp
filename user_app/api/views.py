
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#from user_app import models
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from user_app.api.serializers import RegistrationSerializer
@api_view(['POST',])
def logout_view(request):
    if(request.method=='POST'):
        # request.user.auth_token.delete()
        Refresh_token = request.data["refresh"]
    token = RefreshToken(Refresh_token)
    token.blacklist()
    return Response("Successful Logout", status=status.HTTP_200_OK)
        #RefreshToken(refresh).blacklist()
        
@api_view(['POST',])
def registration_view(request):
    
    if request.method=='POST':
        serializer=RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']="Registration succesfull!"
            data['username']=account.username
            data['email']=account.email
            # token=Token.objects.get(user=account).key
            refresh = RefreshToken.for_user(request.user)
            data['token']={'refresh':str(refresh),'access':str(refresh.access_token)}
            return Response(data)
        else:
            return Response(serializer.errors)
        