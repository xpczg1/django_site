from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название региона")
    code = models.CharField(max_length=10, verbose_name="Код региона", unique=True)

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название роли")
    description = models.TextField(blank=True, verbose_name="Описание роли")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Регион")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        full_name = f"{self.user.last_name} {self.user.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip()


# ТЕПЕРЬ СИГНАЛЫ БУДУТ РАБОТАТЬ, ТАК КАК ТАБЛИЦЫ УЖЕ СОЗДАНЫ
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


class SessionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Время входа")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Время выхода")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    user_agent = models.TextField(verbose_name="User Agent")

    class Meta:
        verbose_name = "История сессии"
        verbose_name_plural = "История сессий"
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"