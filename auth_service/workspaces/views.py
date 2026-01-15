# workspaces/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace
from accounts.models import User

class JoinWorkspaceView(APIView):
    def post(self, request, workspace_id):
        user = request.user
        try:
            ws = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            return Response({"detail": "Workspace not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Ajoute l'utilisateur si pas déjà membre
        ws.members.add(user)
        return Response({"detail": f"{user.email} added to workspace {ws.name}"}, status=status.HTTP_200_OK)
