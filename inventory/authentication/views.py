from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated

# Generate token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Registration View
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'msg': 'Registration successful',
            }, 
            status=status.HTTP_201_CREATED
        )

# Login View
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print('Request', request.data)
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')  # Use validated_data
        password = serializer.validated_data.get('password')  # Use validated_data
        user = authenticate(username=username, password=password)

        print(user)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response(
                {
                    'token': token,
                    'msg': 'Login success',
                }, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'errors': {
                        'non_field_errors': ['Email or Password is not Valid'],
                    }
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
