from main.models import CarAdvert, ThingsAdvert, ServicesAdvert
from .serializers import CarSerializer, ThingSerializer, ServiceSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsOwner


class CarViewSet(ModelViewSet):

    queryset = CarAdvert.objects.all()
    serializer_class = CarSerializer
    filterset_fields = [
        "is_published",
        "is_archive",
    ]

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class ThingViewSet(ModelViewSet):

    queryset = ThingsAdvert.objects.all()
    serializer_class = ThingSerializer
    filterset_fields = [
        "is_published",
        "is_archive",
    ]

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class ServicesViewSet(ModelViewSet):

    queryset = ServicesAdvert.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = [
        "is_published",
        "is_archive",
    ]

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
