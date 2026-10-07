from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory

class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123"}
    """
    def post(self, request):
        # 1. Validacion de datos de entrada (Adapter)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        datos = serializer.validated_data
        
        try:
            # 2. Inyeccion de Dependencias (Factory)
            gateway = PaymentFactory.get_processor()
            
            # 3. Ejecucion de Logica de Negocio (Service Layer)
            servicio = CompraService(procesador_pago=gateway)
            
            # Noten como el servicio NO cambia, solo cambia quien lo llama.
            # Convertimos libro_id a una lista de diccionarios, ya que CompraService
            # espera lista_productos según run.py/services.py (con nombre y precio).
            # Para esto, necesitamos consultar el libro en la base de datos:
            from tienda_app.models import Libro
            libro = Libro.objects.get(id=datos['libro_id'])
            
            # Mock del producto para el servicio existente que usa un objeto
            class ProductoAdaptado:
                def __init__(self, nombre, precio):
                    self.nombre = nombre
                    self.precio = precio
            
            productos = [ProductoAdaptado(libro.titulo, float(libro.precio))]
            
            # El usuario de la petición o uno por defecto
            usuario = request.user.username if request.user.is_authenticated else "UsuarioAnonimo"
            
            resultado = servicio.ejecutar_proceso_compra(
                usuario=usuario,
                lista_productos=productos,
                direccion=datos['direccion_envio']
            )
            
            # Descontar inventario (Lógica simulada para el entregable)
            libro.stock_actual -= 1
            libro.save()
            
            return Response({
                "estado": "exito",
                "mensaje": f"Orden creada. Total: {resultado}"
            }, status=status.HTTP_201_CREATED)
            
        except Libro.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            # Errores de negocio (ej: Sin stock)
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            # Errores inesperados
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
