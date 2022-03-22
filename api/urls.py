from rest_framework.routers import DefaultRouter
from . import views

app_name = "api"

router = DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'things', views.ThingViewSet)
router.register(r'services', views.ServicesViewSet)

urlpatterns = router.urls
