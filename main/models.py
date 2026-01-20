from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator


class RolesManager(models.Manager):
    def get_by_natural_key(self, name_role):
        return self.get(Name_Role=name_role)


class Roles(models.Model):
    ID_Role = models.AutoField(primary_key=True)
    Name_Role = models.CharField(max_length=50, unique=True, verbose_name='Название роли')

    objects = RolesManager()

    def natural_key(self):
        return (self.Name_Role,)

    def __str__(self):
        return self.Name_Role

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class CustomUserManager(BaseUserManager):
    def create_user(self, Login, password=None, **extra_fields):
        if not Login:
            raise ValueError('Логин должен быть указан')

        if 'ID_Role' not in extra_fields:
            try:
                user_role = Roles.objects.get(Name_Role='user')
                extra_fields['ID_Role'] = user_role
            except Roles.DoesNotExist:
                user_role = Roles.objects.create(Name_Role='user')
                extra_fields['ID_Role'] = user_role

        user = self.model(Login=Login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if 'ID_Role' not in extra_fields:
            try:
                admin_role = Roles.objects.get(Name_Role='admin')
                extra_fields['ID_Role'] = admin_role
            except Roles.DoesNotExist:
                admin_role = Roles.objects.create(Name_Role='admin')
                extra_fields['ID_Role'] = admin_role

        return self.create_user(Login, password, **extra_fields)


class Users(AbstractBaseUser, PermissionsMixin):
    ID_User = models.AutoField(primary_key=True)
    ID_Role = models.ForeignKey(
        Roles,
        on_delete=models.CASCADE,
        verbose_name='Роль пользователя'
    )
    Name = models.CharField(max_length=50, verbose_name='Имя')
    Surname = models.CharField(max_length=50, verbose_name='Фамилия')
    Patronymic = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    Login = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Логин',
        validators=[MinLengthValidator(4)]
    )
    # НЕТ поля Password - оно наследуется из AbstractBaseUser

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'Login'
    REQUIRED_FIELDS = ['Name', 'Surname']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.Surname} {self.Name} {self.Patronymic}".strip()

    @property
    def full_name(self):
        return f"{self.Surname} {self.Name} {self.Patronymic}".strip()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.Name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'