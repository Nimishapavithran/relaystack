import time

from celery import shared_task
from django.utils import timezone

from .models import WorkflowExecution


@shared_task
def execute_workflow(execution_id):

    execution = WorkflowExecution.objects.get(
        id=execution_id
    )

    execution.status = "running"
    execution.started_at = timezone.now()

    execution.logs.append(
        {
            "event": "Workflow execution started"
        }
    )

    execution.save()

    try:

        # Simulated workflow execution
        time.sleep(5)

        execution.logs.append(
            {
                "event": "Workflow completed successfully"
            }
        )

        execution.status = "success"

    except Exception as e:

        execution.logs.append(
            {
                "event": str(e)
            }
        )

        execution.status = "failed"

    execution.completed_at = timezone.now()

    execution.save()