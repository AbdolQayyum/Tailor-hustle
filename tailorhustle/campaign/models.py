from django.db import models


# Create your models here.
from user.models import User


class BrandCampaign(models.Model):
    brand = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, unique=True)
    text = models.TextField()

    class Meta:
        verbose_name_plural = 'Campaign'

    def __str__(self):
        return self.title


class UserCampaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(BrandCampaign, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'User Campaign List'

    def __str__(self):
        return f"{self.user.email} - {self.campaign.title}"