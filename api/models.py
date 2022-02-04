from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from dateutil.relativedelta import relativedelta
from datetime import date


GENDER_CHOICES = (
    ('MALE', 'мужской'),
    ('FEMALE', 'женский'),
)


class Product(models.Model):
    name = models.CharField('Наименование продукта', max_length=200,)
    current_volume = models.PositiveIntegerField('Текущий объем',)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Reservoir(models.Model):
    name = models.CharField('Наименование резервуара', max_length=200,)
    capacity = models.PositiveIntegerField('Ёмкость',)

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
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='batches',
        verbose_name='Продукт',)
    number = models.PositiveIntegerField('Номер',)
    date_of_delivery = models.DateTimeField(
        'Дата и время поставки',
        auto_now_add=True,
        )
    tonnage = models.PositiveIntegerField('Тоннаж',)
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='batches',
        verbose_name='Поставщик',
        )
    volume = models.PositiveIntegerField('Объём',)
    reservoir = models.ForeignKey(
        Reservoir,
        on_delete=models.CASCADE,
        related_name='batches',
        verbose_name='Резервуар',
        )
    _density = models.FloatField('Плотность', db_column='density',
                                 editable=False,)
    shift_accepted = models.PositiveIntegerField(
        'Принявшая смена',
        editable=False,
        null=True,
        blank=True,
        )

    class Meta:
        verbose_name = 'Партия'
        verbose_name_plural = 'Партии'

    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        """Вычисление плотности"""
        self._density = self.volume / self.tonnage

    def save(self, *args, **kwargs):
        self.density = self.density
        try:
            last_object = Shift.objects.latest('date_of_beginning')
            self.shift_accepted = last_object.id
        except ObjectDoesNotExist:
            self.shift_accepted = None
        super(Batch, self).save(*args, **kwargs)

    def __str__(self):
        return f'Номер {self.number}'


class Employee(models.Model):
    last_name = models.CharField(
        'Фамилия',
        max_length=200,
        help_text='Введите фамилию сотрудника'
        )
    first_name = models.CharField(
        'Имя',
        max_length=200,
        help_text='Введите имя сотрудника'
        )
    third_name = models.CharField(
        'Отчество',
        max_length=200,
        help_text='Введите отчество сотрудника'
        )
    date_of_employment = models.DateField('Дата устройства на работу',)
    date_of_dismissal = models.DateField(
        'Дата увольнения',
        blank=True,
        null=True,
        )
    gender = models.CharField(
        'Пол',
        max_length=6,
        choices=GENDER_CHOICES,
        default="мужской",
        )
    _experience = models.IntegerField(
        'Опыт',
        db_column='experience',
        editable=False,
        )
    birth_date = models.DateField('Дата рождения',)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        """Вычисление стажа работы сотрудника"""
        self._experience = relativedelta(
            self.date_of_dismissal or date.today(),
            self.date_of_employment
            ).years

    def save(self, *args, **kwargs):
        self.experience = self.experience
        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Shift(models.Model):
    employees = models.ManyToManyField(
        Employee,
        related_name='employees',
        verbose_name='Сотрудники',
        )
    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        related_name='shifts',
        verbose_name='Партия',
        null=True,
        )
    date_of_beginning = models.DateTimeField(
        'Дата и время начала смены',
        auto_now_add=True,
        )
    end_date = models.DateTimeField(
        'Дата и время конца смены',
        blank=True,
        null=True
        )
    current_volume = models.FloatField(
        'Фактический объём продуктов у смены',
        editable=False,
        null=True,
        )
    begin_vol_of_prod = models.FloatField(
        'Объем продуктов на начало смены',
        editable=False,
        null=True,
        )
    end_delta_vol_of_prod = models.FloatField(
        'Дельта объёмов продуктов на конец смены',
        editable=False,
        null=True,
        )

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'

    def __str__(self):
        return f'Принявшая смену с {self.date_of_beginning}'


class Sale(models.Model):
    volume = models.PositiveIntegerField('Объём',)
    date_of_delivery = models.DateTimeField(
        'Дата и время продажи',
        auto_now_add=True
        )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Смена',
        )

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
