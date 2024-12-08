from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import DatabaseError
from django.db.models import Count, Sum, Q
from datetime import timedelta
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import *
from Account.models import Order, OrderItem, CartItem
from Account.serializers import OrderItemSerializer, OrderSerializer, CartItemSerializer
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random

# =============================================== Add Card, Order Product, Add Address, Apply Coupon =============================================================

class OrderViewSet(ViewSet):
    """
    Order operations: Place order and list user orders.
    """

    def list(self, request):
        """
        List all orders of the authenticated user.
        """
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Place an order using cart items and clear the cart.
        """
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'message': 'Cart is empty!'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            shipping_address=request.data.get('shipping_address', 'Default Address'),
        )

        # Create OrderItems and link to Order
        for item in cart_items:
            OrderItem.objects.create(
                user=user,
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price * item.quantity
            )

        # Clear the cart
        cart_items.delete()

        return Response({'message': 'Order placed successfully!', 'order_id': order.id}, status=status.HTTP_201_CREATED)

class CartViewSet(ViewSet):
    """
    Cart operations: Add, View, and Clear cart.
    """

    def list(self, request):
        """
        View all cart items for the authenticated user.
        """
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Add a product to the cart or update the quantity if it already exists.
        """
        user = request.user
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)

        # Check if product already in cart
        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        return Response({'message': 'Product added to cart successfully!'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Remove a specific item from the cart or clear the entire cart.
        """
        user = request.user
        if pk:
            # Delete a specific cart item
            cart_item = get_object_or_404(CartItem, id=pk, user=user)
            cart_item.delete()
            return Response({'message': 'Cart item removed successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Clear entire cart
            CartItem.objects.filter(user=user).delete()
            return Response({'message': 'Cart cleared successfully!'}, status=status.HTTP_204_NO_CONTENT)


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
            serializer = OrderSerializer(order, data={}, partial=True)
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

#========================================================== Views Implementing handle ============================================================================

class TagsViewsHandleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(detail=True, methods=['post'], url_path='add-view')
    def add_view(self, request, pk=None):
        try:
            # Fetch the TypesOfCategory object
            tag = self.get_object()
            # Increment the views
            tag.views += 1
            tag.save()
            # Return success response
            return Response({"message": "View added successfully", "views": tag.views}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductsViewsHandleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'], url_path='add-view')
    def add_view(self, request, pk=None):
        try:
            # Fetch the TypesOfCategory object
            product = self.get_object()
            # Increment the views
            product.views += 1
            product.save()
            # Return success response
            return Response({"message": "View added successfully", "views": product.views}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewsHandleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['post'], url_path='add-view')
    def add_view(self, request, pk=None):
        try:
            # Fetch the TypesOfCategory object
            category = self.get_object()
            # Increment the views
            category.views += 1
            category.save()
            # Return success response
            return Response({"message": "View added successfully", "views": category.views}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TypesOfCategoryViewsHandleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypesOfCategory.objects.all()
    serializer_class = TypeOFCategorySerializer

    @action(detail=True, methods=['post'], url_path='add-view')
    def add_view(self, request, pk=None):
        try:
            # Fetch the TypesOfCategory object
            types_of_category = self.get_object()
            # Increment the views
            types_of_category.views += 1
            types_of_category.save()
            # Return success response
            return Response({"message": "View added successfully", "views": types_of_category.views}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ============================================================Type of Category Wise API's ========================================================================

class BrandWiseProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()

    @action(detail=False, methods=['get'], url_path='by-brand/(?P<brand_id>[^/.]+)')
    def by_category(self, request, brand_id=None):
        product = Product.objects.filter(brand__id=brand_id).distinct()
        if not product.exists():
            return Response({"error": "No product for this Brand."}, status=404)
        serializer = ProductSerializer(product, many=True, context={'request': request})
        return Response(serializer.data)

class TypesOfCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypesOfCategory.objects.all()
    serializer_class = TypeOFCategorySerializer

    @action(detail=False, methods=['get'], url_path=r'exclude/(?P<subcategory_id>\d+)')
    def exclude_category(self, request, subcategory_id=None):
        # Exclude the category with the given ID
        categorytypes = TypesOfCategory.objects.exclude(id=subcategory_id)

        # Pass the request context to the serializer
        serializer = TypeOFCategorySerializer(categorytypes, many=True, context={'request': request})
        
        return Response(serializer.data)

class TypeOfCategoryWiseBrandsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypesOfCategory.objects.all()

    @action(detail=False, methods=['get'], url_path='by-types-of-category/(?P<typeofcategory_id>[^/.]+)')
    def by_category(self, request, typeofcategory_id=None):
        brands = Brand.objects.filter(typeofcategory__id=typeofcategory_id).distinct()
        if not brands.exists():
            return Response({"error": "No brands for this type of category."}, status=404)
        serializer = BrandSerializer(brands, many=True, context={'request': request})
        return Response(serializer.data)

class TypesOfCategoryWiseAllProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()

    @action(detail=False, methods=['get'], url_path='by-types-of-category/(?P<typesofcategory_id>[^/.]+)')
    def by_category(self, request, typesofcategory_id=None):
        products = Product.objects.filter(categorytype__id=typesofcategory_id).distinct()
        if not products.exists():
            return Response({"error": "No products for this category."}, status=404)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

# ======================================================= Home Page Category Wise API's ==========================================================================

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['brand__name']  # Filter by brand name

    @action(detail=False, methods=['get'], url_path='filter-by-brands')
    def filter_by_brands(self, request):
        brand_names = request.query_params.get('brands', None)
        
        if brand_names:
            brand_names_list = brand_names.split(',')  # Split brands by comma
            # Filter products by a list of brands
            products = Product.objects.filter(brand__name__in=brand_names_list)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "At least one brand name is required."}, status=400)

class CategoryWiseAllProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_id>[^/.]+)')
    def by_category(self, request, category_id=None):
        products = Product.objects.filter(category__id=category_id).distinct()
        if not products.exists():
            return Response({"error": "No products for this category."}, status=404)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryWiseBrandsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_id>[^/.]+)')
    def by_category(self, request, category_id=None):
        brands = Brand.objects.filter(category__id=category_id).distinct()
        if not brands.exists():
            return Response({"error": "No brands for this category."}, status=404)
        serializer = BrandSerializer(brands, many=True, context={'request': request})
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Add a custom action to exclude a specific category by its ID
    @action(detail=False, methods=['get'], url_path=r'exclude/(?P<category_id>\d+)')
    def exclude_category(self, request, category_id=None):
        # Exclude the category with the given ID
        categories = Category.objects.exclude(id=category_id)
        # Serialize the categories
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

class ProductSearchViewSet(viewsets.ViewSet):
    """
    A ViewSet for searching products and their details.
    """

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '')  # Search query

        # Validate the query parameter
        if not query:
            return Response(
                {"detail": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Search in Product name and related ProductDetails fields
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(product_details__description__icontains=query) |
                Q(product_details__key_ingredients__icontains=query) |
                Q(product_details__key_benefits__icontains=query)
            ).distinct()

            # Serialize Product without including ProductDetails
            result = ProductSerializer(products, many=True).data

            return Response(result)

        except DatabaseError as db_error:
            # Handle database errors
            return Response(
                {"detail": "A database error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Handle other unexpected errors
            return Response(
                {"detail": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductDetailsViewSet(viewsets.ViewSet):
    """
    A ViewSet for retrieving product information for a specific product.
    """

    @action(detail=False, methods=['get'], url_path='(?P<product_id>[^/.]+)')
    def list_by_product(self, request, product_id=None):
        product_details = ProductDetails.objects.filter(product_id=product_id)
        
        if not product_details.exists():
            return Response({"error": "No product information found for this product."}, status=404)

        serializer = ProductDetailsSerializer(product_details, many=True, context={'request': request})
        return Response(serializer.data, status=200)

class ProductInformationViewSet(viewsets.ViewSet):
    """
    A ViewSet for retrieving product information for a specific product.
    """

    @action(detail=False, methods=['get'], url_path='(?P<product_id>[^/.]+)')
    def list_by_product(self, request, product_id=None):
        product_information = ProductInformation.objects.filter(product_id=product_id)
        
        if not product_information.exists():
            return Response({"error": "No product information found for this product."}, status=404)

        serializer = ProductInformationSerializer(product_information, many=True, context={'request': request})
        return Response(serializer.data, status=200)

class ProductModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ManufacturerModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

def make_messages(request):
    return HttpResponse("This is the messages page.")

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=['get'], url_path='product/(?P<product_id>[^/.]+)')
    def list_by_product(self, request, product_id=None):
        # Filter reviews by product ID
        reviews = Review.objects.filter(product_id=product_id)
        
        if not reviews.exists():
            return Response({"error": "No reviews found for this product."}, status=404)

        # Calculate total review count and total rating count
        total_reviews_count = reviews.count()
        total_rating_count = reviews.aggregate(Sum('rating'))['rating__sum'] or 0

        # Calculate the average rating
        average_rating = total_rating_count / total_reviews_count if total_reviews_count > 0 else 0

        # Count ratings for each star (1-5)
        rating_count = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')

        # Calculate percentages for each rating
        ratings_percentage = []
        for rating in range(1, 6):
            count = next((item['count'] for item in rating_count if item['rating'] == rating), 0)
            percentage = (count / total_reviews_count) * 100 if total_reviews_count > 0 else 0
            ratings_percentage.append({
                "rating": rating,
                "percentage": round(percentage, 2)
            })

        # Prepare the response data
        review_summary = ProductReviewSummarySerializer({
            'total_reviews_count': total_reviews_count,
            'total_rating_count': total_rating_count,
            'average_rating': round(average_rating, 2),  # Add average rating
            'ratings_breakdown': ratings_percentage,
            'reviews': reviews
        })

        return Response(review_summary.data)

# class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     @action(detail=False, methods=['get'], url_path='product/(?P<product_id>[^/.]+)')
#     def list_by_product(self, request, product_id=None):
#         # Filter reviews by product ID
#         reviews = Review.objects.filter(product_id=product_id)
#         if not reviews.exists():
#             return Response({"error": "No reviews found for this product."}, status=404)

#         serializer = self.get_serializer(reviews.first())  # Pass the first review for ratings breakdown
#         return Response(serializer.data)

class ProductHighlightViewSet(viewsets.ViewSet):
    """
    A ViewSet for retrieving images for a specific product.
    """

    @action(detail=False, methods=['get'], url_path='(?P<product_id>[^/.]+)')
    def list_by_product(self, request, product_id=None):
        # Corrected the filter to use 'Product_id'
        product_highlight = ProductHighlight.objects.filter(Product_id=product_id)
        
        if not product_highlight.exists():
            return Response({"error": "No highlights found for this product."}, status=404)

        # Pass the request context to the serializer
        serializer = ProductHighlightSerializer(product_highlight, many=True, context={'request': request})
        return Response(serializer.data, status=200)

class ProductImageViewSet(viewsets.ViewSet):
    """
    A ViewSet for retrieving images for a specific product.
    """

    @action(detail=False, methods=['get'], url_path='(?P<product_id>[^/.]+)')
    def list_by_product(self, request, product_id=None):
        product_images = ProductImage.objects.filter(product_id=product_id)
        if not product_images.exists():
            return Response({"error": "No images found for this product."}, status=404)

        # Pass the request context to the serializer
        serializer = ProductImageSerializer(product_images, many=True, context={'request': request})
        return Response(serializer.data, status=200)

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

        serializer = ProductImageSerializer(data=request.data)
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
    
class PersonalCareModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(tags__name="personal care").distinct()
    
class CollagenAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(tags__name="collagen").distinct()

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
#         order = Order.objects.create(
#             user=user, total_price=0, shipping_address=shipping_address, status='pending'
#         )

#         # Create OrderItems
#         for item in cart_items:
#             try:
#                 product = Product.objects.get(id=item['product_id'])
#                 quantity = item['quantity']

#                 # Use `discounted_price` if available; otherwise, fallback to `selling_price`
#                 product_price = product.discounted_price if product.discounted_price else product.selling_price
#                 item_total_price = product_price * quantity
#                 total_price += item_total_price

#                 OrderItem.objects.create(order=order, product=product, quantity=quantity, price=item_total_price)
#             except Product.DoesNotExist:
#                 return Response({
#                     "success": False,
#                     "message": f"Product ID {item['product_id']} not found."
#                 }, status=status.HTTP_404_NOT_FOUND)

#         discount = 0
#         if coupon_code:
#             try:
#                 coupon = Coupons.objects.get(code=coupon_code)
#                 if coupon.is_valid(total_price, cart_items, is_first_order=not Order.objects.filter(user=user).exists()):
#                     discount = coupon.apply_discount(total_price)
#                     order.total_price = total_price - discount
#                     coupon.used_count += 1
#                     coupon.save()
#                 else:
#                     return Response({
#                         "success": False,
#                         "message": "Coupon conditions not met."
#                     }, status=status.HTTP_400_BAD_REQUEST)
#             except Coupons.DoesNotExist:
#                 return Response({
#                     "success": False,
#                     "message": "Invalid coupon code."
#                 }, status=status.HTTP_404_NOT_FOUND)
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

class CategoryMobileViewSet(viewsets.ReadOnlyModelViewSet):
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
    
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        type_of_category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=type_of_category_id)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()  # Correct: This is a queryset, which is iterable
    serializer_class = CountrySerializer

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
class CategoryMobileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Apply distinct first, then limit the result in memory
        categories = (
            Category.objects.filter(tags__name="mobile application popular categories")
            .order_by('id')  # Ensures consistent ordering
            .distinct()
        )
        return categories[:16]  # Limit the queryset to the first 16 results

    # @action(detail=True, methods=['get'])
    # def types(self, request, pk=None):
    #     category = self.get_object()
    #     types_of_category = TypesOfCategory.objects.filter(category=category)
    #     serializer = TypeOFCategorySerializer(types_of_category, many=True)
    #     return Response(serializer.data)

    # @action(detail=True, methods=['get'], url_path='types/(?P<type_id>[^/.]+)/products')
    # def products(self, request, pk=None, type_id=None):
    #     products = Product.objects.filter(type_of_category_id=type_id)
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)


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