from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ContactsView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("product_detail/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path("product_create/", ProductCreateView.as_view(), name='product_create'),
    path("product_update/<int:pk>/", ProductUpdateView.as_view(), name='product_update'),
    path("product_delete/<int:pk>/", ProductDeleteView.as_view(), name='product_delete'),
    path("category/", CategoryListView.as_view(), name='category_list')
]
