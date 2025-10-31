from django.contrib import admin

from network_link.models import ContactInfo, NetworkNode, Product


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели ContactInfo.
    Отображает основные поля контакта.
    """

    list_display = ["email", "country", "city", "street", "house_number"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели Product.
    Отображает название, модель и дату выпуска продукта.
    """

    list_display = ["name", "model", "product_release_date"]


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели NetworkNode.
    Отображает основные поля звена сети и предоставляет действие по сбросу задолженности.
    """

    list_display = ["name", "contact_info", "supplier", "debt", "created_at"]
    list_filter = ["contact_info__city"]
    readonly_fields = ["created_at"]

    def reset_debt_action(self, request, queryset):
        """
        Действие для сброса задолженности у выбранных объектов.

        Args:
            request (HttpRequest): Объект запроса.
            queryset (QuerySet): Набор объектов для обновления.
        """
        queryset.update(debt=0.00)

    reset_debt_action.short_description = "Очистить задолженность у выбранных объектов"
    actions = [reset_debt_action]
