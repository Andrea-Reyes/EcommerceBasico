from django.shortcuts import render, redirect
from django.http import Http404
from .forms import ProductoForm
import requests

FIREBASE_BASE_URL = 'https://ecommercebasico-2b261-default-rtdb.firebaseio.com/productos'

def index(request): 
    response = requests.get(f'{FIREBASE_BASE_URL}.json')
    data = response.json() or {}

    productos = []
    for key, value in data.items():
        productos.append({
            'id': key,
            'nombre': value.get('nombre'),
            'descripcion': value.get('descripcion'),
            'precio': value.get('precio'),
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
            }
            requests.post(f'{FIREBASE_BASE_URL}.json', json=data)
            return redirect('index')
    else:
        form = ProductoForm()

    return render(request, 'formulario.html', {'form': form})