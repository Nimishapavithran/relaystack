from rest_framework import generics, permissions

from .models import Workflow
from .serializers import WorkflowSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import (
    Workflow,
    WorkflowExecution,
)

from .tasks import execute_workflow

from .serializers import (
    WorkflowSerializer,
    WorkflowExecutionSerializer,
)

class WorkflowListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = WorkflowSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):

        return Workflow.objects.filter(
            workspace__members__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )
class WorkflowExecuteView(APIView):

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, workflow_id):

        workflow = Workflow.objects.get(
            id=workflow_id
        )

        execution = WorkflowExecution.objects.create(
            workflow=workflow,
            status="pending",
        )

        execute_workflow.delay(
            str(execution.id)
        )

        serializer = WorkflowExecutionSerializer(
            execution
        )

        return Response(
            serializer.data,
            status=status.HTTP_202_ACCEPTED
        )        