from django.urls import path, include
from Medicine.views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'medicines', MedicineHomePageViewSet, basename='medicine get A to Z first digit to search') # url = medicine/filter/<str:first_char>/
# router.register(f'medicines', MedicineAllViewSet, basename="all Medicines")

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Filter PrizeAndMedicineDetail based on medicine_id
    path('api/prizes/filter/<int:medicine_id>/', PrizeAndMedicineDetailFilterView.as_view(), name='prize-filter'),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)