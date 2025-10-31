from django.core.exceptions import ValidationError
from django.db import models


class ContactInfo(models.Model):
    """
    Модель контактов.
    Содержит информацию о стране, городе, улице и номере дома.
    """

    email = models.EmailField(unique=True, verbose_name="Email пользователя")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    def __str__(self):
        return (
            f"Адресс: {self.country}, {self.city}, {self.street}, {self.house_number}"
        )


class Product(models.Model):
    """
    Модель продукта.
    Содержит название, модель и дату выпуска продукта.
    """

    name = models.CharField(max_length=100, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель продукта")
    product_release_date = models.DateField()

    def __str__(self):
        return f"Адресс: {self.name}, {self.model}"


class NetworkNode(models.Model):
    """
    Модель звена сети.
    Содержит информацию о поставщике, продуктах, задолженности и уровне в иерархии.
    """

    LEVEL_CHOICES = [
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "ИП"),
    ]
    name = models.CharField(max_length=100, verbose_name="Название продукта")
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Проверяет, что звено не является поставщиком самого себя.
        """
        if self.supplier and self.supplier == self:
            raise ValidationError("Поставщик не может быть самим собой.")

    def __str__(self):
        return self.name

    def get_level(self):
        """
        Вычисляет уровень звена в иерархии.

        Returns:
            int: Уровень звена (0 - завод, 1 - розничная сеть, 2 - ИП и т. д.).
        """
        level = 0
        current = self
        while current.supplier:
            level += 1
            current = current.supplier
        return level
