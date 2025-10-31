from rest_framework import serializers

from .models import ContactInfo, NetworkNode, Product


class ContactInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ContactInfo.
    Используется для преобразования объектов ContactInfo в JSON и обратно.
    """

    class Meta:
        model = ContactInfo
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    Используется для преобразования объектов Product в JSON и обратно.
    """

    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.
    Поддерживает вложенные объекты ContactInfo и Product.
    """

    contact_info = ContactInfoSerializer()
    products = ProductSerializer(many=True, required=False)

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ["debt"]

    def create(self, validated_data):
        """
        Создаёт новый объект NetworkNode с вложенными связями.

        Args:
            validated_data (dict): Данные для создания объекта.

        Returns:
            NetworkNode: Созданный объект NetworkNode.
        """
        contact_data = validated_data.pop("contact_info")
        contact = ContactInfo.objects.create(**contact_data)

        products_data = validated_data.pop("products", [])
        node = NetworkNode.objects.create(contact_info=contact, **validated_data)

        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            node.products.add(product)

        return node

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект NetworkNode с вложенными связями.

        Args:
            instance (NetworkNode): Объект, который нужно обновить.
            validated_data (dict): Данные для обновления.

        Returns:
            NetworkNode: Обновлённый объект NetworkNode.
        """
        contact_data = validated_data.pop("contact_info", None)
        if contact_data:
            contact = instance.contact_info
            for attr, value in contact_data.items():
                setattr(contact, attr, value)
            contact.save()

        products_data = validated_data.pop("products", None)
        if products_data is not None:
            instance.products.clear()
            for product_data in products_data:
                product, created = Product.objects.get_or_create(**product_data)
                instance.products.add(product)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
