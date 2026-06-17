from django.urls import path

from .views import WorkflowListCreateView,WorkflowExecuteView

urlpatterns = [

    path(
        "",
        WorkflowListCreateView.as_view(),
        name="workflow-list-create",
    ),
    path(
    "<uuid:workflow_id>/execute/",
    WorkflowExecuteView.as_view(),
    name="workflow-execute",
),
]