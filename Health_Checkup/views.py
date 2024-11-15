#views
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *

# View operations
class CategoryListView(generics.ListAPIView):
    queryset = Category_s.objects.all()
    serializer_class = CategorysSerializer

class PackageListView(generics.ListAPIView):
    serializer_class = HealthsPackageSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Health_Packages.objects.filter(category_id=category_id)

class PackageDetailView(generics.RetrieveAPIView):
    queryset = Health_Packages.objects.all()
    serializer_class = HealthsPackageSerializer
    lookup_field = 'id'


# post operations
class CreateCategoryView(generics.CreateAPIView):
    queryset = Category_s.objects.all()
    serializer_class = CategorysSerializer

class CreateTestView(generics.CreateAPIView):
    queryset = Test_s.objects.all()
    serializer_class = TestsSerializer

class CreateHealthPackageView(generics.CreateAPIView):
    queryset = Health_Packages.objects.all()
    serializer_class = HealthsPackageSerializer



# # View for handling test details
# class TestDetailViewSet(viewsets.ModelViewSet):
#     queryset = TestDetail.objects.all()
#     serializer_class = TestDetailSerializer





























































































