from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from .models import NetworkNode
from .permissions import IsActiveEmployee
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели NetworkNode.
    Обеспечивает CRUD-операции с фильтрацией по стране и проверкой прав доступа.
    """

    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["contact_info__country"]

    def get_permissions(self):
        """
        Возвращает список классов разрешений для каждого запроса.

        Returns:
            list: Список объектов разрешений.
        """
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
