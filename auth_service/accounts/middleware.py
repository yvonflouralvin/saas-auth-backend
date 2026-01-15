# accounts/middleware.py
import jwt
from django.conf import settings
from workspaces.models import Workspace

class JWTWorkspaceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("Authorization", None)
        request.workspace = None
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id") or payload.get("sub")

                # Si le token contient workspace_id, on l'utilise
                ws_id = payload.get("workspace_id")
                if ws_id:
                    ws = Workspace.objects.filter(id=ws_id, members__id=user_id).first()
                else:
                    # sinon premier workspace assigné
                    ws = Workspace.objects.filter(members__id=user_id).first()
                
                request.workspace = ws
            except Exception:
                pass
        return self.get_response(request)
