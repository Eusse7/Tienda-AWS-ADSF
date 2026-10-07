from django.shortcuts import render
from tienda_app.models import Libro

def inventario_view(request):
    libros = Libro.objects.all()
    return render(request, 'tienda_app/inventario.html', {'libros': libros})
