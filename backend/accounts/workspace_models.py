import uuid
from django.db import models


class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)

    owner = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="owned_workspaces"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name