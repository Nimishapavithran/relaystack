from rest_framework import serializers

from .models import (
    Workflow,
    WorkflowExecution,
)


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow

        fields = "__all__"

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]


class WorkflowExecutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkflowExecution

        fields = "__all__"