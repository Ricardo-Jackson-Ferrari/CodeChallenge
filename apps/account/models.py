from django.db import models
from .utils import generate_ref_code

class SimpleUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    ip_address = models.GenericIPAddressField(null=True)


class Profile(models.Model):
    user = models.OneToOneField(SimpleUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(SimpleUser, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> None:
        return self.user

    def get_recommened_profiles(self):
        pass

    def save(self, args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code

        super().save(args, **kwargs)
