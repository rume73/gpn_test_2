from django.db import models

from .validators import validate_positive


GENDER_CHOICES = (
    ('MALE', 'male'),
    ('FEMALE', 'female'),
)


class Product(models.Model):
    name = models.CharField('Наименование продукта', max_length=200,)
    current_volume = models.PositiveIntegerField(
        'Текущий объем',
        validators=[validate_positive],
        )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField('Наименование резервуара', max_length=200,)
    capacity = models.PositiveIntegerField(
        'Ёмкость',
        validators=[validate_positive],
        )

    class Meta:
        verbose_name = 'Резервуар'
        verbose_name_plural = 'Резервуары'

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField('Наименование поставщика', max_length=200,)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

    def __str__(self):
        return self.name


class Batch(models.Model):
    products = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Продукт',)
    number = models.PositiveIntegerField(
        'Номер',
        validators=[validate_positive],
        )
    date_of_delivery = models.DateTimeField('Дата и время поставки',)
    tonnage = models.PositiveIntegerField(
        'Тоннаж',
        validators=[validate_positive],
        )
    provider = models.CharField('Провайдер', max_length=200,)
    volume = models.PositiveIntegerField(
        'Объём',
        validators=[validate_positive],
        )
    objects = models.ForeignKey(
        Object,
        on_delete=models.CASCADE,
        related_name='objects',
        verbose_name='Резервуар',)
    density = 
    shift_accepted = 


class Employee(models.Model):
    full_name = models.CharField(
        'ФИО',
        max_length=200,
        help_text='Введите ФИО сотрудника'
        )
    date_of_employment = models.DateField('Дата устройства на работу',)
    date_of_dismissal = models.DateField(
        'Дата увольнения',
        blank=True,
        null=True,
        )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default="MALE",
        )
    experience = 
    date_of_birth = models.DateField('Дата рождения',)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name


class Shift(models.Model):
    employees = models.ManyToManyField(
        Employee,
        related_name='employees',
        verbose_name='Сотрудник',
        )
    batchs = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='batchs',
        verbose_name='Партии',
        )
    date_of_delivery = models.DateTimeField('Дата и время начала смены',)
    begin_vol_of_prod =
    end_delta_vol_of_prod =

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'


class Sale(models.Model):
    volume = models.PositiveIntegerField(
        'Объём',
        validators=[validate_positive],
        )
    date_of_delivery = models.DateTimeField('Дата и время продажи',)
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name='shifts',
        verbose_name='Смены',
        )

    class Meta:
        verbose_name = 'Продажа'
