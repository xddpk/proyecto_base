class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito", {})
        if not carrito:
            carrito = self.session["carrito"] = {}
        
        self.carrito = carrito
            
    def agregar (self, producto):
        id = str(producto.id)
        if id not in self.carrito:
            self.carrito[id]= {
                "producto_id": producto.id,
                "nombre" : producto.nombre_producto,
                "acumulado": producto.precio_producto,
                "stock" : producto.stock_producto,
                "cantidad":1,
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["acumulado"] += producto.precio_producto
        self.guardar_carrito()
            
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
        
    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()
            
    def restar (self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= producto.precio_producto
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()
    def limpiar (self):
        self.session["carrito"] = {}
        self.session.modified = True
        
    def get_cantidad(self, producto_id):
        id = str(producto_id)
        if id in self.carrito:
            return self.carrito[id]["cantidad"]
        return 0
    def esta_vacio(self):
        return not bool(self.carrito)