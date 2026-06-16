from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
)
from .models import (
    User,
    Workspace,
    WorkspaceMember,
    
)

class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer

    permission_classes = [permissions.AllowAny]


class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
class WorkspaceCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = WorkspaceSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        workspace = serializer.save(
            owner=request.user
        )

        WorkspaceMember.objects.create(
            workspace=workspace,
            user=request.user,
            role="owner"
        )

        return Response(
            WorkspaceSerializer(workspace).data,
            status=status.HTTP_201_CREATED
        )


class WorkspaceListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        workspaces = Workspace.objects.filter(
            members__user=request.user
        ).distinct()

        serializer = WorkspaceSerializer(
            workspaces,
            many=True
        )

        return Response(serializer.data)    