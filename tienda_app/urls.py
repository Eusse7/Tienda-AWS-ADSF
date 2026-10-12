from django.urls import path
from tienda_app.api.views import CompraAPIView, ProductoListView
from tienda_app.views import inventario_view

urlpatterns = [
    path('inventario/', inventario_view, name='inventario'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
    path('api/v1/productos/', ProductoListView.as_view(), name='api_productos'),
    path('api/v1/productos', ProductoListView.as_view(), name='api_productos_noslash'),
]
