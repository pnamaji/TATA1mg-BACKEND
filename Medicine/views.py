from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .models import *
from .serializers import *
from .serializers import MedicineSerializer

class FactBoxDetailFilterView(generics.ListAPIView):

    serializer_class = FactBoxSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = FactBox.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class QuickTipDetailFilterView(generics.ListAPIView):

    serializer_class = QuickTipSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = QuickTip.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class MissedDoseDetailFilterView(generics.ListAPIView):

    serializer_class = MissedDoseSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = MissedDose.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class SafetyAdviceDetailFilterView(generics.ListAPIView):

    serializer_class = SafetyAdviceSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = SafetyAdvice.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class HowToDrugWorksDetailFilterView(generics.ListAPIView):

    serializer_class = HowDrugWorkSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = HowDrugWork.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class HowToUseDetailFilterView(generics.ListAPIView):

    serializer_class = HowToUseSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = HowToUse.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class SideEffectsDetailFilterView(generics.ListAPIView):

    serializer_class = SideEffectSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = SideEffect.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class UseAndBenefitsDetailFilterView(generics.ListAPIView):

    serializer_class = UseCaseSerializer
    
    def get_queryset(self):
        medicine_id = self.kwargs.get('medicine_id')
        queryset = UseCase.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class OverviewDetailFilterView(generics.ListAPIView):
    """
    API view to filter PrizeAndMedicineDetail by the `medicine_id`.
    """
    serializer_class = OverviewSerializer
    
    def get_queryset(self):
        """
        Optionally restrict the returned PrizeAndMedicineDetail based on
        the `medicine_id` provided in the URL.
        """
        medicine_id = self.kwargs.get('medicine_id')
        queryset = Overview.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset

class PrizeAndMedicineDetailFilterView(generics.ListAPIView):
    """
    API view to filter PrizeAndMedicineDetail by the `medicine_id`.
    """
    serializer_class = PrizeAndMedicineDetailSerializer
    
    def get_queryset(self):
        """
        Optionally restrict the returned PrizeAndMedicineDetail based on
        the `medicine_id` provided in the URL.
        """
        medicine_id = self.kwargs.get('medicine_id')
        queryset = PrizeAndMedicineDetail.objects.all()

        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
        
        return queryset
    
class MedicineHomePageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    @action(detail=False, methods=['get'], url_path='filter/(?P<first_char>.+)')
    def filter_by_first_char(self, request, first_char=None):
        """
        Custom action to filter medicines by the first character (digit or letter).
        """
        medicines = Medicine.objects.filter(name__istartswith=first_char)
        
        if medicines.exists():
            serializer = MedicineSerializer(medicines, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {"message": f"No medicines found starting with '{first_char}'"},
            status=status.HTTP_404_NOT_FOUND,
        )