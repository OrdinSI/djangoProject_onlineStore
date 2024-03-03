
from catalog.apps import CatalogConfig
from django.urls import path
from catalog.views import ProductListView, ProductDetailView, ContactsView


app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path("contacts/", ContactsView.as_view(), name='contacts'),
    path("product_detail/<int:pk>/", ProductDetailView.as_view(), name='product_detail')
]
