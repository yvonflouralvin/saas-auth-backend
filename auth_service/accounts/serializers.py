# accounts/serializers.py
from rest_framework import serializers
from .models import User
from workspaces.models import Workspace
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from workspaces.models import Workspace

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        # 1️⃣ Créer l'utilisateur
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

        # 2️⃣ Créer workspace par défaut
        default_workspace = Workspace.objects.create(
            name=f"{user.email}-workspace",
            owner=user
        )
        default_workspace.members.add(user)

        # 3️⃣ Ajouter workspace actif dans JWT
        refresh = RefreshToken.for_user(user)
        refresh["workspace_id"] = str(default_workspace.id)
        refresh["workspace_name"] = default_workspace.name

        self.context["tokens"] = {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

        return user


# 🔑 Custom Login pour inclure workspace actif
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Workspace actif = premier workspace assigné
        workspace = Workspace.objects.filter(members=user).first()
        if workspace:
            data["workspace_id"] = str(workspace.id)
            data["workspace_name"] = workspace.name

            # Ajouter workspace dans payload JWT
            refresh = self.get_token(user)
            refresh["workspace_id"] = str(workspace.id)
            refresh["workspace_name"] = workspace.name
            data["refresh_token"] = str(refresh)
            data["access_token"] = str(refresh.access_token)

        return data
