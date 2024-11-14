from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def post(self, request, product_id, *args, **kwargs):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImageProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)  # Associate the image with the specified product
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class PopularCategoriesAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Filter products with the "Health Concerns" tag
#         popular_category = Category.objects.filter(tags__name="popular catagories").distinct()

#         # Serializer the filtered category
#         serializer = CategorySerializer(popular_category, many=True)
#         return Response(serializer.data)
    
class PopularCategoriesModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(tags__name="popular catagories").distinct()

# class PersonalCareAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Filter products with the "Health Concerns" tag
#         personal_category = Category.objects.filter(tags__name="personal care").distinct()

#         # Serializer the filtered category
#         serializer = CategorySerializer(personal_category, many=True)
#         return Response(serializer.data)
    
class PersonalCareModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(tags__name="personal care").distinct()

# class CollagenAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Filter products with the "Health Concerns" tag
#         collagen_category = Product.objects.filter(tags__name="collagen").distinct()

#         # Serializer the filtered category
#         serializer = ProductSerializer(collagen_category, many=True)
#         return Response(serializer.data)
    
class CollagenAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(tags__name="collagen").distinct()

# class HealthConcernAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Filter products with the "Health Concerns" tag
#         healthconcerns_category = Category.objects.filter(tags__name="Health Concerns").distinct()

#         # Serializer the filtered category
#         serializer = CategorySerializer(healthconcerns_category, many=True)
#         return Response(serializer.data)
    
class HealthConcernAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        Override the get_queryset method to filter products by the 'Spotlite' tag.
        """
        return Category.objects.filter(tags__name="Health Concerns").distinct()
    
class SpotlightProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Override the get_queryset method to filter products by the 'Spotlite' tag.
        """
        return Product.objects.filter(tags__name="spotlight").distinct()

# class SpotlightProductListAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Filter products with the "Spotlite" tag
#         spotlite_products = Product.objects.filter(tags__name="spotlight").distinct()
        
#         # Serialize the filtered products
#         serializer = ProductSerializer(spotlite_products, many=True)
#         return Response(serializer.data)
    
class CategoryProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Fetch all Category objects
        category_types = Category.objects.all()

        # Select a random category type
        random_category_type = random.choice(category_types)

        # Serializer the selected category and its products
        serializer = CategorySerializer(random_category_type)
        return Category.objects.filter(id=random_category_type.id)
    
class CategoryTypeProductView(viewsets.ReadOnlyModelViewSet):
    queryset = TypesOfCategory.objects.all()
    serializer_class = TypeOFCategorySerializer

    def get_queryset(self):
        # Fetch all TypesOfCategory objects
        category_types = TypesOfCategory.objects.all()

        # Select a random category type
        random_category_type = random.choice(category_types)

        # Return a queryset that contains just the random category
        return TypesOfCategory.objects.filter(id=random_category_type.id)


# class OrderCreateAPIView(APIView):
#     """
#     API View to create an order and apply a coupon if available.
#     """

#     def post(self, request):
#         user = request.user
#         cart_items = request.data.get('cart_items', [])
#         coupon_code = request.data.get('coupon_code', None)
#         shipping_address = request.data.get('shipping_address', '')

#         if not cart_items:
#             return Response(
#                 {"success": False, "message": "No items in cart."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         total_price = 0
#         order = Order.objects.create(
#             user=user,
#             total_price=0,  # We'll update it after calculating discounts
#             shipping_address=shipping_address,
#             status='pending'
#         )

#         # Create OrderItems and calculate total
#         for item in cart_items:
#             product = get_object_or_404(Product, id=item['product_id'])
#             quantity = item['quantity']
#             price = product.price * quantity
#             total_price += price

#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=quantity,
#                 price=price
#             )

#         discount = 0
#         # Apply coupon if provided
#         if coupon_code:
#             try:
#                 coupon = Coupon.objects.get(
#                     code=coupon_code,
#                     valid_from__lte=timezone.now(),
#                     valid_to__gte=timezone.now()
#                 )
#                 # Assuming `is_valid` method in Coupon model handles all conditions
#                 if coupon.is_valid(total_price, cart_items, is_first_order=not Order.objects.filter(user=user).exists()):
#                     discount = coupon.get_discount(total_price)
#                     order.total_price = total_price - discount
#                     coupon.used_count += 1
#                     coupon.save()
#                 else:
#                     return Response(
#                         {"success": False, "message": "Coupon conditions not met."},
#                         status=status.HTTP_400_BAD_REQUEST
#                     )
#             except Coupon.DoesNotExist:
#                 return Response(
#                     {"success": False, "message": "Invalid coupon code."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#         else:
#             order.total_price = total_price

#         order.save()

#         return Response({
#             "success": True,
#             "order_id": order.id,
#             "total_price": total_price,
#             "discount": discount,
#             "final_total": order.total_price,
#             "message": "Order created successfully."
#         }, status=status.HTTP_201_CREATED)

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = request.data.get('cart_items', [])
        coupon_code = request.data.get('coupon_code', None)
        shipping_address = request.data.get('shipping_address', '')

        if not cart_items:
            return Response({"success": False, "message": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        order = Order.objects.create(user=user, total_price=0, shipping_address=shipping_address, status='pending')

        # Create OrderItems
        for item in cart_items:
            try:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                price = product.price * quantity
                total_price += price

                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            except Product.DoesNotExist:
                return Response({"success": False, "message": f"Product ID {item['product_id']} not found."}, status=status.HTTP_404_NOT_FOUND)

        discount = 0
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid(total_price, cart_items, is_first_order=not Order.objects.filter(user=user).exists()):
                    discount = coupon.apply_discount(total_price)
                    order.total_price = total_price - discount
                    coupon.used_count += 1
                    coupon.save()
                else:
                    return Response({"success": False, "message": "Coupon conditions not met."}, status=status.HTTP_400_BAD_REQUEST)
            except Coupon.DoesNotExist:
                return Response({"success": False, "message": "Invalid coupon code."}, status=status.HTTP_404_NOT_FOUND)
        else:
            order.total_price = total_price

        order.save()
        return Response({
            "success": True,
            "order_id": order.id,
            "total_price": total_price,
            "discount": discount,
            "final_total": order.total_price,
            "message": "Order created successfully."
        }, status=status.HTTP_201_CREATED)



class CouponApplyAPIView(APIView):
    """
    API View to apply a coupon and calculate the discount based on conditions.
    """

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        cart_items = request.data.get('cart_items', [])

        if not cart_items:
            return Response(
                {"success": False, "message": "No items in cart."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total amount from cart items
        total_amount = sum(item['price'] for item in cart_items)
        is_first_order = not Order.objects.filter(user=request.user).exists()
        products = [get_object_or_404(Product, id=item['product_id']) for item in cart_items]

        try:
            # Find the coupon if it exists and is within the valid date range
            coupon = Coupon.objects.get(code=code, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())

            # Check if the coupon is valid
            if coupon.is_valid(total_amount, products, is_first_order):
                discount = 0

                # Calculate discount based on coupon type
                if coupon.is_percentage:
                    discount = total_amount * (coupon.discount / 100)
                else:
                    discount = coupon.discount

                # Update coupon usage count if needed
                coupon.used_count += 1
                coupon.save()

                # Send successful response with discount details
                return Response({
                    "success": True,
                    "discount": discount,
                    "final_total": total_amount - discount,
                    "message": f"Coupon '{code}' applied successfully."
                }, status=status.HTTP_200_OK)
            else:
                # Invalid coupon usage for this cart or conditions not met
                return Response({
                    "success": False,
                    "message": "Coupon not valid for cart items or does not meet requirements."
                }, status=status.HTTP_400_BAD_REQUEST)

        except Coupon.DoesNotExist:
            # Invalid coupon code
            return Response({
                "success": False,
                "message": "Invalid coupon code."
            }, status=status.HTTP_404_NOT_FOUND)
        

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user field to the currently authenticated user
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Custom action to get TypesOfCategory by Category
    @action(detail=True, methods=['get'])
    def types(self, request, pk=None):
        try:
            # Retrieve the category by primary key (ID) or add additional filtering as needed
            category = self.get_object()  # will automatically use pk
            # Filter TypesOfCategory based on this category
            types_of_category = TypesOfCategory.objects.filter(category=category)
            serializer = TypeOFCategorySerializer(types_of_category, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)
        
class TypeOfCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TypeOFCategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return TypesOfCategory.objects.filter(category_id=category_id)
    
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        type_of_category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=type_of_category_id)

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, sku):
        product = get_object_or_404(Product, sku=sku)
        # Pass the request context to the serializer
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

# ViewSet for Category
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def types(self, request, pk=None):
        category = self.get_object()
        types_of_category = TypesOfCategory.objects.filter(category=category)
        serializer = TypeOFCategorySerializer(types_of_category, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='types/(?P<type_id>[^/.]+)/products')
    def products(self, request, pk=None, type_id=None):
        products = Product.objects.filter(type_of_category_id=type_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# API View to get types of category based on category
class TypeOfCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):
        # Fetch types based on category_id
        types_of_category = TypesOfCategory.objects.filter(category_id=category_id)
        serializer = TypeOFCategorySerializer(types_of_category, many=True)
        return Response(serializer.data)


# API View to get products filtered by type of category
class ProductAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, type_of_category_id):
        # Fetch products based on type_of_category_id
        products = Product.objects.filter(categorytype_id=type_of_category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)