"""
URL configuration for jewellery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
# from jewelleryapp.views import GoogleLogin, GoogleLoginCallback, LoginPage
from django.conf import settings 
from django.conf.urls.static import static
from jewelleryapp.views import*
urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('',include('jewelleryapp.urls')),
    # path("login/", LoginPage.as_view(), name="login"),
    # path("api/v1/auth/", include("dj_rest_auth.urls")),
    # path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    # path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    # path(
    #     "api/v1/auth/google/callback/",
    #     GoogleLoginCallback.as_view(),
    #     name="google_login_callback",
    # ),
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
