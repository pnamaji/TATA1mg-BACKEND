from django.shortcuts import render
from django.core.cache import cache
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
from rest_framework import generics, permissions
from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random

class Minimum33PercentOffProductsList(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            return Product.objects.filter(
                discount_percentage__gte="33"
            ).distinct()
        except Product.DoesNotExist:
            return Product.objects.none()  # Return an empty queryset if no products are found
        except Exception as e:
            # Log the error and return an empty queryset
            print(f"Error fetching products: {e}")
            return Product.objects.none()

class HomeopathyWomensHealthProductsList(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            return Product.objects.filter(
                tags__name="homeopathy"
            ).filter(
                tags__name="women"
            ).filter(
                tags__name="Health Care"
            ).distinct()
        except Product.DoesNotExist:
            return Product.objects.none()  # Return an empty queryset if no products are found
        except Exception as e:
            # Log the error and return an empty queryset
            print(f"Error fetching products: {e}")
            return Product.objects.none()

class HealthCareDevicesTopBrandsList(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_queryset(self):
        try:
            return Brand.objects.filter(
                tags__name="top brands"
            ).filter(
                tags__name="healthcare devices"
            ).distinct()
        except Brand.DoesNotExist:
            return Brand.objects.none()  # Return an empty queryset if no products are found
        except Exception as e:
            # Log the error and return an empty queryset
            print(f"Error fetching brands: {e}")
            return Brand.objects.none()

class ZanduTopSellersProducts(viewsets.ReadOnlyModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            return Product.objects.filter(
                tags__name="top seller", 
                brand__name="Zandu"
            ).distinct()
        except Product.DoesNotExist:
            return Product.objects.none()  # Return an empty queryset if no products are found
        except Exception as e:
            # Log the error and return an empty queryset
            print(f"Error fetching products: {e}")
            return Product.objects.none()

class TATA1mgHealthProducts(viewsets.ReadOnlyModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            return Product.objects.filter(
                tags__name="Health Care", 
                brand__name="TATA_1mg"
            ).distinct()
        except Product.DoesNotExist:
            return Product.objects.none()  # Return an empty queryset if no products are found
        except Exception as e:
            # Log the error and return an empty queryset
            print(f"Error fetching products: {e}")
            return Product.objects.none()

class DealsOfTheDayProductsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):

        cache_key = 'deals_of_the_day_random_products'
        products = cache.get(cache_key)

        if not products:

            products = Product.objects.filter(tags__name="deals of the day").distinct()
            products = random.sample(list(products), min(len(products), 5))

            cache.get(cache_key, products, 60 * 60 * 24)
        return products

class AyurvedaTopBrandsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_queryset(self):
        return Brand.objects.filter(tags__name="top ayurvedic brands").distinct()

class ExploreSomethingNewProductsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):

        cache_key = 'something_new_random_products'
        products = cache.get(cache_key)

        if not products:

            products = Product.objects.filter(tags__name="something new").distinct()
            products = random.sample(list(products), min(len(products), 5))

            cache.get(cache_key, products, 60 * 60 * 24)
        return products

class TrendingProductsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):

        cache_key = 'trending_random_products'
        products = cache.get(cache_key)

        if not products:

            products = Product.objects.filter(tags__name="trending").distinct()
            products = random.sample(list(products), min(len(products), 5))

            cache.get(cache_key, products, 60 * 60 * 24)
        return products

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
    
class PainReliefAndCoughAndColdModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):

        cache_key = 'pain_relief_cough_and_cold_random_products'
        products = cache.get(cache_key)

        if not products:
            # Fetch products from both categories
            cold_and_cough_products = Product.objects.filter(category__name="Cold & Cough").distinct()
            pain_relief_products = Product.objects.filter(category__name="Pain Relief").distinct()

            # Combine the products from both categories
            combined_products = cold_and_cough_products | pain_relief_products

            products = random.sample(list(combined_products), min(len(combined_products), 5))

            cache.get(cache_key, products, 60 * 60 * 24)
        return products
    
class ComboDealsProductsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):

        cache_key = 'combo_deals_random_products'
        products = cache.get(cache_key)

        if not products:

            products = Product.objects.filter(tags__name="combo deals").distinct()
            products = random.sample(list(products), min(len(products), 5))

            cache.get(cache_key, products, 60 * 60 * 24)
        return products
    
class SkinCareProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Cache key to store the random products for 24 hours
        cache_key = 'skin_care_random_products'
        products = cache.get(cache_key)

        if not products:
            # If cache is empty, select random products and cache them for 24 hours
            products = Product.objects.filter(categorytype__name="Skin Care").distinct()
            products = random.sample(list(products), min(len(products), 5))  #e.g., get 5 random products

            # Store products in cache for 24 hours
            cache.set(cache_key, products, 60 * 60 * 24)
        return products
    
class SuperSavingDealsModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Cache key to store the random products for 24 hours
        cache_key = 'popular_lab_tests_random_products'
        products = cache.get(cache_key)

        if not products:
            # If cache is empty, select random products and cache them for 24 hours
            products = Product.objects.filter(tags__name="popular lab tests").distinct()
            products = random.sample(list(products), min(len(products), 5))  # e.g., get 5 random products

            # Store products in cache for 24 hours
            cache.set(cache_key, products, 60 * 60 * 24)

        return products

class PopularLabTestModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(tags__name="popular lab tests").distinct()
    
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
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         cart_items = request.data.get('cart_items', [])
#         coupon_code = request.data.get('coupon_code', None)
#         shipping_address = request.data.get('shipping_address', '')

#         if not cart_items:
#             return Response({"success": False, "message": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST)

#         total_price = 0
#         order = Order.objects.create(user=user, total_price=0, shipping_address=shipping_address, status='pending')

#         # Create OrderItems
#         for item in cart_items:
#             try:
#                 product = Product.objects.get(id=item['product_id'])
#                 quantity = item['quantity']
#                 price = product.price * quantity
#                 total_price += price

#                 OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
#             except Product.DoesNotExist:
#                 return Response({"success": False, "message": f"Product ID {item['product_id']} not found."}, status=status.HTTP_404_NOT_FOUND)

#         discount = 0
#         if coupon_code:
#             try:
#                 coupon = Coupon.objects.get(code=coupon_code)
#                 if coupon.is_valid(total_price, cart_items, is_first_order=not Order.objects.filter(user=user).exists()):
#                     discount = coupon.apply_discount(total_price)
#                     order.total_price = total_price - discount
#                     coupon.used_count += 1
#                     coupon.save()
#                 else:
#                     return Response({"success": False, "message": "Coupon conditions not met."}, status=status.HTTP_400_BAD_REQUEST)
#             except Coupon.DoesNotExist:
#                 return Response({"success": False, "message": "Invalid coupon code."}, status=status.HTTP_404_NOT_FOUND)
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
        order = Order.objects.create(
            user=user, total_price=0, shipping_address=shipping_address, status='pending'
        )

        # Create OrderItems
        for item in cart_items:
            try:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']

                # Use `discounted_price` if available; otherwise, fallback to `selling_price`
                product_price = product.discounted_price if product.discounted_price else product.selling_price
                item_total_price = product_price * quantity
                total_price += item_total_price

                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=item_total_price)
            except Product.DoesNotExist:
                return Response({
                    "success": False,
                    "message": f"Product ID {item['product_id']} not found."
                }, status=status.HTTP_404_NOT_FOUND)

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
                    return Response({
                        "success": False,
                        "message": "Coupon conditions not met."
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Coupon.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "Invalid coupon code."
                }, status=status.HTTP_404_NOT_FOUND)
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


class OrderCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            # Fetch the order to be canceled
            order = Order.objects.get(id=order_id, user=request.user)

            # Check if the order is already canceled or completed
            if order.status in ['canceled', 'completed']:
                return Response({
                    "success": False,
                    "message": "Order cannot be canceled as it is already processed."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Serialize and update the order status to "canceled"
            serializer = OrderCancelSerializer(order, data={}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Order canceled successfully.",
                    "order": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Order.DoesNotExist:
            return Response({
                "success": False,
                "message": "Order not found."
            }, status=status.HTTP_404_NOT_FOUND)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch orders only for the logged-in user
        return Order.objects.filter(user=self.request.user).order_by('-order_date')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

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
        types_of_category = TypesOfCategory.objects.filter(id=category_id)
        serializer = TypeOFCategorySerializer(types_of_category, many=True)
        return Response(serializer.data)


# API View to get products filtered by type of category
class ProductAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, type_of_category_id):
        # Fetch products based on type_of_category_id
        products = Product.objects.filter(id=type_of_category_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)