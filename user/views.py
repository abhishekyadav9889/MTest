from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
import pytz

from .models import UserProfile
from .serializers import UserProfileSerializer, TimezoneConverterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Returns the permission based on the type of action"""

        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class UserLogIn(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class TimezoneConverter(APIView):

    def post(self, request):

        serializer = TimezoneConverterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            input_time = data['time']

            timezone = None
            if data['timezone'] == 'UK':
                timezone = pytz.timezone('Europe/London')
            if data['timezone'] == 'Philippines':
                timezone = pytz.timezone('Asia/Manila')

            if data['timezone'] == 'US':
                timezone = pytz.timezone('America/New_York')

            time = input_time.astimezone(timezone)
         
            response_data = {
                data['timezone']: time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            }

            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# m.roshan@giglabz.com
# 9562745899