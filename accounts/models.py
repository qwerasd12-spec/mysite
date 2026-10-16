from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=50, blank=True, verbose_name="전공/학과")
    student_id = models.CharField(max_length=20, blank=True, verbose_name="학번/사번")
    address = models.CharField(max_length=100, blank=True, verbose_name="주소")
    phone = models.CharField(max_length=20, blank=True, verbose_name="전화번호")
    bio = models.TextField(blank=True, verbose_name="자기소개")

    def __str__(self):
        return f"{self.user.username}의 프로필"

# 유저가 생성될 때 자동으로 Profile도 함께 생성되도록 설정하는 시그널
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
