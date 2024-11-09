from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import *
from Account.models import *
from django.shortcuts import get_object_or_404
from rest_framework.generics import get_object_or_404


# Operations for category model
class CategoryCreateView(APIView):
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def delete(self, request):
        Category.objects.all().delete()
        return Response({"message": "All categories have been deleted."}, status=status.HTTP_204_NO_CONTENT)


class CategoryDetailView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class CategoryUpdateView(APIView):
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteView(APIView):
    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Operations for Experience model


# List all experiences or create a new experience
class ExperienceListCreateView(APIView):
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Retrieve, update, or delete a single experience by ID
class ExperienceDetailView(APIView):
    def get(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)

    def put(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# Operations for FAQ

class FAQListCreateView(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a single FAQ by ID
class FAQDetailView(APIView):
    def get(self, request, pk):
        faq = get_object_or_404(FAQ, pk=pk)
        serializer = FAQSerializer(faq)
        return Response(serializer.data)

    def put(self, request, pk):
        faq = get_object_or_404(FAQ, pk=pk)
        serializer = FAQSerializer(faq, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        faq = get_object_or_404(FAQ, pk=pk)
        serializer = FAQSerializer(faq, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        faq = get_object_or_404(FAQ, pk=pk)
        faq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  

class UserContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve the user's contact details."""
        try:
            user_contact = UserContact.objects.get(user=request.user)
            serializer = UserContactSerializer(user_contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserContact.DoesNotExist:
            return Response({'detail': 'User contact not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Create or update user's contact details."""
        try:
            # Fetch the mobile number from UserData
            user_data = UserData.objects.get(user=request.user)
            mobile_number = user_data.mobile_number
        except UserData.DoesNotExist:
            return Response({'detail': 'User data not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user contact already exists
        user_contact, created = UserContact.objects.get_or_create(user=request.user)
        serializer = UserContactSerializer(user_contact, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            # Update phone number from UserData and save the record
            serializer.save(phone_number=mobile_number)
            message = "User contact created successfully!" if created else "User contact updated successfully!"
            return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                  


# User Selected Plans 
class SelectPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        user = request.user

        # Check if the plan exists
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already selected this plan
        existing_plan = UserPlan.objects.filter(user=user, plan=plan, is_active=True).first()
        if existing_plan:
            return Response({"message": "You have already selected this plan"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the user's selected plan
        user_plan = UserPlan.objects.create(user=user, plan=plan)
        serializer = UserPlanSerializer(user_plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# # Companies can view User selected plans
# class PlanUsersAPIView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request, plan_id):
#         # Check if the plan exists
#         try:
#             plan = Plan.objects.get(id=plan_id)
#         except Plan.DoesNotExist:
#             return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Fetch users who selected this plan
#         user_plans = UserPlan.objects.filter(plan=plan)
#         serializer = UserPlanDetailSerializer(user_plans, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


#Companies registration and their plans views
class MedicalPartnerView(APIView):
    def get(self, request):
        partners = MedicalPartner.objects.all()
        serializer = MedicalPartnerSerializer(partners, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MedicalPartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanView(APIView):
    def get(self, request):
        plans = Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanDetailView(APIView):
    def get(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        serializer = PlanSerializer(plan)
        return Response(serializer.data)

    def put(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan = get_object_or_404(Plan, pk=pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserPlanListView(APIView):
    permission_classes = [IsAdminUser]  # Restrict access to admin users only

    def get(self, request, plan_id=None):
        if plan_id:
            user_plans = UserPlan.objects.filter(plan_id=plan_id)
        else:
            user_plans = UserPlan.objects.all()
        serializer = UserPlanSerializer(user_plans, many=True)
        return Response(serializer.data)






