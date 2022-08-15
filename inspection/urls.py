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
from django.urls import path,include
import authapp.urls
import property.urls
import mrequest.urls
import emergency.urls
import report.urls
import property.views as property_view


from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('openapi/', get_schema_view(
        title="Inspection endpoints",
        description="API endpoints for inspection api"
    ), name='openapi-schema'),

    path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    
    path('api/',include(authapp.urls)),
    path('api/',include(property.urls)),
     path('api/',include(emergency.urls)),
      path('api/',include(mrequest.urls)),
 path('api/',include(report.urls)),   
 path('api/user/property/', property_view.UserProperty.as_view()) 
    
    
]


