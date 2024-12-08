from django.urls import path, include
from Products.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

# ====================================================== Home Page API's ====================================================================================

router.register(r'categories', CategoryMobileViewSet, basename='Mobile application category')
router.register(r'api/categorytypewiseproducts', CategoryTypeProductView, basename='Category Type wise Products')
router.register(r'api/categorywiseproducts', CategoryProductView, basename='Category Wise Products')
router.register(r'api/spotlight', SpotlightProductViewSet, basename='Spotlight Product List')
router.register(r'api/healthconcerns', HealthConcernAPIView, basename='Health Concerns Categories List')
router.register(r'api/collagen', CollagenAPIView, basename='Collagen tag Products List')
router.register(r'api/personalcare', PersonalCareModelViewSet, basename='Personal Care tag Category List')
router.register(r'api/popularcategories', PopularCategoriesModelViewSet, basename='Popular Categories List')
router.register(r'api/popularlabtestsproducts', PopularLabTestModelViewSet, basename='Popular Lab Test Products List')
router.register(r'api/supersavingdeals', SuperSavingDealsModelViewSet, basename='Super saving deals products list')
router.register(r'api/skincareproducts', SkinCareProductModelViewSet, basename='Skin Care Type of Category Products List')
router.register(r'api/combodealsproducts', ComboDealsProductsModelViewSet, basename='Combo Deals Tag Products List')
router.register(r'api/painrelief&coughandcold', PainReliefAndCoughAndColdModelViewSet, basename="Pain Relief & Cough and Cold Category Products")
router.register(r'api/trendingproducts', TrendingProductsModelViewSet, basename="Trending Products")
router.register(r'api/exploresomethingnewproducts', ExploreSomethingNewProductsModelViewSet, basename="Explore Something New Products")
router.register(r'api/topayurvedabrands', AyurvedaTopBrandsModelViewSet, basename="Top Ayurveda Brands")
router.register(r'api/dealsofthedayproducts', DealsOfTheDayProductsModelViewSet, basename="Deals of the Day Products")
router.register(r'api/tata1mg-health-products', TATA1mgHealthProducts, basename="Health Products of TATA 1mg Brand")
router.register(r'api/zandu-top-seller-products', ZanduTopSellersProducts, basename="Zandu Top Seller Products")
router.register(r'api/healthcare-devices-top-brands', HealthCareDevicesTopBrandsList, basename="Healthcare Devices top Brands")
router.register(r'api/homeopathy-womens-health', HomeopathyWomensHealthProductsList, basename="Homeopathy Women's health Products")
router.register(r'api/minimum-33-off-products', Minimum33PercentOffProductsList, basename="Minimum 33 or more percent off Products")
router.register(r'api', ProductSearchViewSet, basename='product-search')            # URL IS products/api/search/?q=<input>

# ======================================================= Specific products API's =====================================================================

router.register(r'api/products', ProductModelViewSet)
router.register(r'api/product-images', ProductImageViewSet, basename='product-image')
router.register(r'api/product-highlights', ProductHighlightViewSet, basename='product-Highlights')
router.register(r'api/product-rating', ReviewViewSet, basename='product Rating')    # this is url /products/api/product-rating/product/<int:product_id>/
router.register(r'api/product-details', ProductDetailsViewSet, basename='product details')    # this is url /products/api/product-details/<int:product_id>/
router.register(r'api/product-information', ProductInformationViewSet, basename='other Information')    # this is url /products/api/other-rating/<int:product_id>/

# ============================================================= Category Wise ==================================================================================

router.register(r'api/categories', CategoryViewSet, basename='category')         # URL for exclude /products/api/categories/exclude/<category_id>/                        you can get this url through type of categories and you can exclude category list
router.register(r'api/brands', CategoryWiseBrandsViewSet, basename='Category Wise Brands')     # URL products/api/brands/by-category/<category_id>/
router.register(r'api/all-products', CategoryWiseAllProductsViewSet, basename='Category Wise All Products')     # URL products/api/all-products/by-category/5/

# ==========================================================Type of Category wise ==================================================================================

router.register(r'api/types-of-categories', TypesOfCategoryViewSet, basename='types of category brands')         # URL for exclude /products/api/types-of-categories/exclude/<category_id>/                        you can get this url through type of categories and you can exclude category list
router.register(r'api/all-products', TypesOfCategoryWiseAllProductsViewSet, basename='Types of Category Wise All Products')     # URL products/api/all-products/by-types-of-category/5/
router.register(r'api/brands', TypeOfCategoryWiseBrandsViewSet, basename='Type of Category Wise Brands')     # URL products/api/brands/by-types-of-category/<category_id>/
router.register(r'api/products', BrandWiseProductsViewSet, basename='Brand wise Products')          #  URL products/api/products/by-brand/<brand_id>/

# =========================================================== Handle Views Count ====================================================================================

router.register(r'api/types-of-category', TypesOfCategoryViewsHandleViewSet, basename='types-of-category-handle-views')    # URL products/api/types-of-category/<id>/add-view/
router.register(r'api/category', CategoryViewsHandleViewSet, basename='category-handle-views')    # URL products/api/category/<id>/add-view/
router.register(r'api/product', ProductsViewsHandleViewSet, basename='product-handle-views')    # URL products/api/product/<id>/add-view/
router.register(r'api/tags', TagsViewsHandleViewSet, basename='tags-handle-views')    # URL products/api/tags/<id>/add-view/

# ========================================================== Add Card, Order. address ===================================================================================

router.register(r'api/cart', CartViewSet, basename='cart')
router.register(r'api/orders', OrderViewSet, basename='orders')



router.register(r'api/manufacturer', ManufacturerModelViewSet)
router.register(r'api/brands', BrandViewSet)
router.register(r'api/country', CountryViewSet)

from . import views

urlpatterns = [

    path('', include(router.urls)),
    path('messages/', views.make_messages, name='make_messages'),

    # view Type-of-Category
    # path('category/<int:category_id>/types/', TypeOfCategoryAPIView.as_view(), name='types_of_category'),
    
    # load products 
    # path('category/type/<int:type_of_category_id>/products/', ProductAPIView.as_view(), name='products_by_type'),

    # Get SKU to all data of product
    path('api/products/<str:sku>/', ProductDetailAPIView.as_view(), name='Product Details API View'),

    # Order Products
    # path('api/create-order/', OrderCreateAPIView.as_view(), name='create_order_api'),

    path('api/<int:product_id>/upload-image/', ProductImageUploadView.as_view(), name='upload-product-image'),

    # Cancel order
    path('order/cancel/<int:order_id>/', OrderCancelAPIView.as_view(), name='order-cancel'),

    # view all orders
    path('api/orders/', OrderListView.as_view(), name='order-list'),

    # view order by providing specific id
    path('api/orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),

]
if settings.DEBUG:  # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)