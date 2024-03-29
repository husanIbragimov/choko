from django.urls import path
from apps.product.views import about, shop_list, shop_details, index, shop_images, shop_books, shop_clothes, \
    shop_appliances, PorductDetail, book_detail

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('shop/', shop_list, name="products_filter"),
    path('books/', shop_books, name="books"),
    path('clothes/', shop_clothes, name="clothes"),
    path('techniques/', shop_appliances, name="techniques"),
    path('shop-images/', shop_images, name="shop-images"),
    path('shop-details/<int:pk>/', shop_details, name="shop-details"),
    path('detail/<int:pk>/', PorductDetail.as_view(), ),
    path('shop-details/<int:pk>/', shop_details, name="shop-details"),
    path('book-details/<int:pk>/', book_detail, name="book-details"),
    path('detail/<int:pk>/', PorductDetail.as_view(), )
]
