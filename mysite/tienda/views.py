from django.shortcuts import render, redirect
from django.http import Http404
from .forms import ProductoForm
import requests
from urllib.parse import quote_plus

FIREBASE_BASE_URL = 'https://ecommercebasico-2b261-default-rtdb.firebaseio.com/productos'

def index(request): 
    response = requests.get(f'{FIREBASE_BASE_URL}.json')
    data = response.json() or {}
    DEFAULT_IMAGE = 'https://www.shutterstock.com/image-vector/default-ui-image-placeholder-wireframes-600nw-1037719192.jpg'
    numeroK ='+50236994033'
    numeroP = '+50233234967'
    productos = []
    for key, value in data.items():
        nombre = value.get('nombre')
        mensaje = f"¡Buen día! Quisiera solicitar información sobre el producto '{nombre}'. Gracias."
        whatsapp_url = f"https://api.whatsapp.com/send?phone={numeroP}&text={quote_plus(mensaje)}"
        productos.append({
            'id': key,
            'nombre': nombre,
            'descripcion': value.get('descripcion'),
            'precio': value.get('precio'),
            #'imagenURL': value.get('imagenURL'),
            'imagenURL': DEFAULT_IMAGE if not value.get('imagenURL') else value.get('imagenURL'),
            'whatsappURL': whatsapp_url,
        })

    productos.reverse()
    return render(request, 'index.html', {'productos': productos})

def formulario_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            data = {
                'nombre': form.cleaned_data['nombre'],
                'descripcion': form.cleaned_data['descripcion'],
                'precio': float(form.cleaned_data['precio']),
                'imagenURL': form.cleaned_data['imagenURL'],
            }
            requests.post(f'{FIREBASE_BASE_URL}.json', json=data)
            return redirect('index')
    else:
        form = ProductoForm()

    return render(request, 'formulario.html', {'form': form})