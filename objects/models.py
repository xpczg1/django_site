from django.db import models
from main.models import Users  # импортируем Users из main

class Regions(models.Model):
    ID_Region = models.AutoField(primary_key=True)
    Name_Region = models.CharField(max_length=50, unique=True, verbose_name='Название региона')

    def __str__(self):
        return self.Name_Region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class Objects(models.Model):
    FENCE_TYPES = [
        ('metal mesh', 'Металлическая сетка'),
        ('metal pipes', 'металлические трубы'),
        ('concrete', 'Бетонный'),
        ('other', 'Другой'),
    ]

    ID_Object = models.AutoField(primary_key=True)
    ID_Region = models.ForeignKey(
        Regions,
        on_delete=models.CASCADE,
        verbose_name='Регион'
    )
    Name_Object = models.CharField(max_length=50, verbose_name='Название объекта')
    Perimeter = models.FloatField(verbose_name='Периметр')
    Type_Of_Fence = models.CharField(
        max_length=50,
        choices=FENCE_TYPES,
        verbose_name='Тип ограждения'
    )
    Coordinates = models.CharField(max_length=255, verbose_name='Координаты', null=True, blank=True)

    def __str__(self):
        return self.Name_Object

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

class Session_History(models.Model):
    ID_Session = models.AutoField(primary_key=True)
    ID_User = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='session_histories'
    )
    ID_Object = models.ForeignKey(
        Objects,
        on_delete=models.CASCADE,
        verbose_name='Объект'
    )
    Main_Guard_Surname = models.CharField(max_length=50, verbose_name='Фамилия главного охранника')
    Date = models.DateField(verbose_name='Дата сессии')
    Time = models.TimeField(verbose_name='Время сессии')

    def __str__(self):
        return f"Сессия {self.ID_Session} - {self.Date} {self.Time}"

    class Meta:
        verbose_name = 'История сессии'
        verbose_name_plural = 'История сессий'
        ordering = ['-Date', '-Time']