from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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
        user = self.model(Login=Login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(Login, password, **extra_fields)


class Users(AbstractBaseUser):
    ID_User = models.AutoField(primary_key=True)
    ID_Role = models.ForeignKey(
        Roles,
        on_delete=models.PROTECT,
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
    # Убрано поле Password, так как оно уже есть в AbstractBaseUser

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'Login'
    REQUIRED_FIELDS = ['Name', 'Surname', 'ID_Role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.Surname} {self.Name} {self.Patronymic}".strip()

    @property
    def full_name(self):
        return f"{self.Surname} {self.Name} {self.Patronymic}".strip()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class RegionsManager(models.Manager):
    def get_by_natural_key(self, coordinates):
        return self.get(Coordinates=coordinates)


class Regions(models.Model):
    ID_Region = models.AutoField(primary_key=True)
    Coordinates = models.CharField(max_length=50, unique=True, verbose_name='Координаты')

    objects = RegionsManager()

    def natural_key(self):
        return (self.Coordinates,)

    def __str__(self):
        return f"Регион {self.ID_Region} ({self.Coordinates})"

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class ObjectsManager(models.Manager):
    def get_by_natural_key(self, name_object):
        return self.get(Name_Object=name_object)


class Objects(models.Model):
    FENCE_TYPES = [
        ('wood', 'Деревянный'),
        ('metal', 'Металлический'),
        ('concrete', 'Бетонный'),
        ('chainlink', 'Сетка-рабица'),
        ('other', 'Другой'),
    ]

    ID_Object = models.AutoField(primary_key=True)
    ID_Region = models.ForeignKey(
        Regions,
        on_delete=models.CASCADE,
        verbose_name='Регион'
    )
    Name_Object = models.CharField(max_length=50, verbose_name='Название объекта')
    Length = models.FloatField(verbose_name='Длина')
    Width = models.FloatField(verbose_name='Ширина')
    Type_Of_Fence = models.CharField(
        max_length=50,
        choices=FENCE_TYPES,
        verbose_name='Тип ограждения'
    )

    objects = ObjectsManager()

    def natural_key(self):
        return (self.Name_Object,)

    def __str__(self):
        return self.Name_Object

    @property
    def area(self):
        return self.Length * self.Width

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        unique_together = ('ID_Region', 'Name_Object')


class Session_HistoryManager(models.Manager):
    def get_by_natural_key(self, date, time, id_user):
        return self.get(Date=date, Time=time, ID_User=id_user)


class Session_History(models.Model):
    ID_Session = models.AutoField(primary_key=True)
    ID_User = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    ID_Object = models.ForeignKey(
        Objects,
        on_delete=models.CASCADE,
        verbose_name='Объект'
    )
    Main_Guard_Surname = models.CharField(max_length=50, verbose_name='Фамилия главного охранника')
    Date = models.DateField(verbose_name='Дата сессии')
    Time = models.TimeField(verbose_name='Время сессии')

    objects = Session_HistoryManager()

    def natural_key(self):
        return (self.Date, self.Time, self.ID_User_id)

    def __str__(self):
        return f"Сессия {self.ID_Session} - {self.Date} {self.Time}"

    class Meta:
        verbose_name = 'История сессии'
        verbose_name_plural = 'История сессий'
        unique_together = ('ID_User', 'ID_Object', 'Date', 'Time')
        ordering = ['-Date', '-Time']