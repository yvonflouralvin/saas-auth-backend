# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

# 🔑 Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        tokens = serializer.context["tokens"]
        return Response({
            "user": {"id": str(user.id), "email": user.email},
            "workspace": {
                "id": str(user.workspaces.first().id),
                "name": user.workspaces.first().name
            },
            "access_token": tokens["access"],
            "refresh_token": tokens["refresh"],
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    # utilise serializer par défaut simplejwt
    serializer_class = MyTokenObtainPairSerializer
    pass