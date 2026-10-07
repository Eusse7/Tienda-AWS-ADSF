from tienda_app.domain.builders import OrdenBuilder

class CompraService:
    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()
        
    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: Semantica clara y validacion interna
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_productos(lista_productos)
                 .para_envio(direccion)
                 .build())
                 
        # Uso del Factory (inyectado): Cambio de comportamiento sin cambio de codigo
        if self.procesador.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."
            
        orden.delete()
        raise Exception("Error en la pasarela de pagos.")
