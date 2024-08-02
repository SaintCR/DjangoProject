"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from DjangoProject import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #HOME
    path('', views.home),

    #CRUD CLIENTES
    path('Clientes/insertar', views.clienteinsertar),
    path('Clientes/listado', views.clientelistado),
    path('Clientes/borrar/<int:idcliente>', views.borrarcliente),
    path('Clientes/actualizar/<int:idcliente>', views.clienteactualizar),
    path('Clientes/API/<str:email>', views.clienteAPI),
    #FIN CRUD CLIENTES

    #CRUD CARGO
    path('Cargo/insertar', views.cargoinsertar),
    path('Cargo/listado', views.cargolistado),
    path('Cargo/borrar/<int:idcargo>', views.cargoborrar),
    path('Cargo/actualizar/<int:idcargo>', views.cargoactualizar),
    #FIN CRUD CARGO

    #CRUD PRODUCTOS
    path('Producto/insertar/', views.insertarproducto),
    path('Producto/listado/', views.listadoproducto),
    path('Producto/actualizar/<int:id>', views.productoactualizar),
    path('Producto/borrar/<int:id>', views.borrarproducto),
    #FIN PRODUCTOS

    #CRUD FACTURA
    path('Factura/insertar/', views.facturainsertar),
    #FIN CRUD FACTURA
]
