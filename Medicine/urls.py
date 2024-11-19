from django.urls import path, include
from Medicine.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet, basename='medicine') # url = medicine/filter/<str:first_char>/

urlpatterns = [
    path('api/', include(router.urls)),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)