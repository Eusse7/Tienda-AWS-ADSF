from django.urls import path
from tienda_app.api.views import CompraAPIView
from tienda_app.views import inventario_view

urlpatterns = [
    # ... sus urls antiguas ...
    path('inventario/', inventario_view, name='inventario'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]
