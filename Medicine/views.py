from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .models import *
from .serializers import *
from .serializers import MedicineSerializer

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