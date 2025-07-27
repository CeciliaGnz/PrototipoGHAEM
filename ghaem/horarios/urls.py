from rest_framework.routers import DefaultRouter
from .views import HorarioViewSet

router = DefaultRouter()
router.register(r'horarios', HorarioViewSet, basename='horario')
urlpatterns = router.urls
