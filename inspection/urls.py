"""inspection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include,re_path
import authapp.urls
import property.urls
import mrequest.urls
import emergency.urls
import report.urls
import messaging.urls
import property.views as property_view


#from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
#from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.views.generic.base import TemplateView


class SwaggerPageView(TemplateView):
    template_name = "openapi.json"

schema_view = get_schema_view(
   openapi.Info(
      title="Inspection API",
      default_version='v1',
      description="Inspection schema",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   authentication_classes =[],
   permission_classes=[permissions.AllowAny],
)


#re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
urlpatterns = [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs"),

    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    re_path(
        r"^apis(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path('swagger.json', SwaggerPageView.as_view(), name='schema-json'),
     #re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   
    path('admin/', admin.site.urls),
   
     path('api/',include(messaging.urls)),  
    path('api/',include(authapp.urls)),
    path('api/',include(property.urls)),
     path('api/',include(emergency.urls)),
      path('api/',include(mrequest.urls)),
     path('api/',include(report.urls)), 
 
    
    
]


