
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

schema_url_patterns = [
    path('api/v1/', include('EcomAPI.urls')),
]
schema_view = get_schema_view(
    title='Server  API',
    url='https://www.example.org/api/',
    patterns=schema_url_patterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('EcomAPI.urls')),
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="DRF CRUD",
        description="API for CRUD",
        version="2.0.0"
    ), name='openapi-schema'),

]
