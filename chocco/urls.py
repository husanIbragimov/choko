"""chocco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from apps.base import views
from apps.order.api.v1 import views as api_views
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .schema import swagger_urlpatterns


urlpatterns = [
    # admin
    path('chocolate-admin/', admin.site.urls),

] + swagger_urlpatterns + i18n_patterns(
    # media
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # tokens
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # language
    path('i18n/', include('django.conf.urls.i18n')),
    # lib
    path('base/', include('allauth.urls')),

    # swagger


    # api
    path('api/v1/', include('api.product.urls'), name='product'),
    path('api/v1/', include('api.account.urls'), name='account'),
    path('api/v1/', include('api.contact.urls'), name='contact'),
    path('api/v1/', include('api.order.urls'), name='order'),

    path('change_status/', api_views.change_status),
    path('count-products/', api_views.count_products),
    # local apps
    path('', include('apps.product.urls')),
    path('order/', include('apps.order.urls')),
    path('contact/', include('apps.contact.urls')),
    path('app/v1/', include('apps.product.api.urls')),

    # login & register
    path('register/', views.register, name="register"),
    path('login/', views.login_func, name="login"),
    path('logout/', views.logout_func, name="logout"),


    prefix_default_language=False,
)


if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "chocco.errors.page_not_found_view"
