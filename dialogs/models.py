from django.db import models
from django.urls import reverse


class Dialog(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("dialogs:detail", args=[self.id])


class Query(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    req = models.TextField()
    res = models.TextField()
    is_active = models.BooleanField(default=True)
    total_tokens = models.IntegerField(default=0)

    class Meta:
        get_latest_by = ["id"]

    def get_absolute_url(self):
        return reverse("dialogs:detail", args=[self.dialog.id])
