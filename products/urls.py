from django.urls import path

from products.views import (
    ProductListView, ProductCreateView, ProductDetailView, ProductDeleteView, ProductUpdateView, CategoryListView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView, product_bulk_creation, download_file,
)

app_name = "mailings"

urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list"
    ),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "categories/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
    path(
        "products/create/",
        ProductCreateView.as_view(),
        name="product-create"
    ),
    path(
        "products/create/bulk",
        product_bulk_creation,
        name="product-create-bulk"
    ),
    path(
        "products/bulk-template/download",
        download_file,
        name="product-create-bulk-template-download"
    ),
    path(
        "products/",
        ProductListView.as_view(),
        name="product-list"
    ),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product-detailed"
    ),
    path(
        "products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product-update"
    ),
    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product-delete"
    ),
]
