from django.db import models


class SimpleUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(SimpleUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> None:
        return self.user
