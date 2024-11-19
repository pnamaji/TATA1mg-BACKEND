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
    path('api/overview/filter/<int:medicine_id>/', OverviewDetailFilterView.as_view(), name='Overview filter'),
    path('api/use-and-benefits/filter/<int:medicine_id>/', UseAndBenefitsDetailFilterView.as_view(), name='Use and Benefits filter'),
    path('api/side-effects/filter/<int:medicine_id>/', SideEffectsDetailFilterView.as_view(), name='Side Effects filter'),
    path('api/how-to-use/filter/<int:medicine_id>/', HowToUseDetailFilterView.as_view(), name='How to Use filter'),
    path('api/how-to-drug-works/filter/<int:medicine_id>/', HowToDrugWorksDetailFilterView.as_view(), name='How to Drug works filter'),  # Pending 
    path('api/safety-advice/filter/<int:medicine_id>/', SafetyAdviceDetailFilterView.as_view(), name='Safety Advice filter'),
    path('api/missed-dose/filter/<int:medicine_id>/', MissedDoseDetailFilterView.as_view(), name='Missed Dose filter'),
    path('api/quick-tip/filter/<int:medicine_id>/', QuickTipDetailFilterView.as_view(), name='Quick Tip filter'),
    path('api/fact-box/filter/<int:medicine_id>/', FactBoxDetailFilterView.as_view(), name='Fact Box filter'),
]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)