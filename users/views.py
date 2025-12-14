from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from article_hub.tasks import register_user_log
from users.models import User
from users.serializers import UserCreateSerializer, UserProfileSerializer, UserRegisterResponseSerializer


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = serializer.instance
        print(user)
        register_user_log(user)
        response = UserRegisterResponseSerializer(user)
        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        return response


class UserProfileView(APIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
