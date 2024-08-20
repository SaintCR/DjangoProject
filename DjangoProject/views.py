from django.db import connection
from django.shortcuts import redirect, render
from django.core.serializers import serialize
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



from DjangoProject.models import Cargo, Clientes, Producto, Factura, FacturaHasProducto


def home(request):
    return render(request,'Home/home.html')

#region CLIENTES

def clienteinsertar(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    if request.method == "POST":
        print("Hacemos el guardado en la BD")
        if request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('telefono') and request.POST.get('direccion') and request.POST.get('correoelectronico') and request.POST.get('cargoid'):
            clientes = Clientes()
            clientes.nombres = request.POST.get('nombre')
            clientes.apellidos = request.POST.get('apellido')
            clientes.telefono = request.POST.get('telefono')
            clientes.direccion = request.POST.get('direccion')
            clientes.correoelectronico = request.POST.get('correoelectronico')
            clientes.cargo = Cargo.objects.get(id=request.POST.get('cargoid'))
            clientes.save()
            return redirect('/Clientes/listado')
    else:
        cargos = Cargo.objects.all()
        return render(request, "Clientes/insertar.html",{"cargos":cargos})
    
def clientelistado(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    clientes = Clientes.objects.all()
    return render(request, 'Clientes/listar.html', {'clientes':clientes})

def borrarcliente(request, idcliente):
    cliente = Clientes.objects.filter(id=idcliente)
    cliente.delete()
    return redirect('/Clientes/listado')

def clienteactualizar(request, idcliente):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        correoelectronico = request.POST.get('correoelectronico')
        cargoid = request.POST.get('cargoid')
        
        if nombre and apellido and telefono and direccion and correoelectronico and cargoid:
            cliente = Clientes.objects.get(id=idcliente)
            cliente.nombres = nombre
            cliente.apellidos = apellido
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.correoelectronico = correoelectronico
            cliente.cargo = Cargo.objects.get(id=cargoid)
            cliente.save()
            return redirect('/Clientes/listado')
    else:
        cliente = Clientes.objects.get(id=idcliente)
        cargos = Cargo.objects.all()
        return render(request, "Clientes/actualizar.html", {"cliente": cliente, "cargos": cargos})
    
def clienteAPI(request, email):
    cliente = Clientes.objects.filter(correoelectronico=email)
    jsoncliente = serialize('json', cliente)
    return HttpResponse(jsoncliente, content_type="application/json")

#endregion

#region CARGO

def cargoinsertar(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    if request.method == "POST":
        if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('descuento'):
            insertar = connection.cursor()
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            descuento = request.POST.get('descuento')
            insertar.execute("call insertarcargo('"+nombre+"','"+descripcion+"','"+descuento+"')")
            
            return redirect('/Cargo/listado')
    else:
        return render(request, "Cargo/insertar.html")
    
def cargolistado(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    cargos = connection.cursor()
    cargos.execute('call listadocargo()')
    return render(request, 'Cargo/listar.html',{'cargos':cargos})

def cargoborrar(request,idcargo):
    borrar = connection.cursor()
    borrar.execute("call borrarcargo('"+str(idcargo)+"')")
    return redirect('/Cargo/listado')

def cargoactualizar(request,idcargo):
    if request.method == "POST":
        if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('descuento'):
            insertar = connection.cursor()
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            descuento = request.POST.get('descuento')
            insertar.execute("call actualizarcargo('"+str(idcargo)+"','"+nombre+"','"+descripcion+"','"+descuento+"')")
            return redirect('/Cargo/listado')
    else:
        uncargo = connection.cursor()
        uncargo.execute("call consultaruncargo('"+str(idcargo)+"')")
        return render(request, 'Cargo/actualizar.html',{"uncargo":uncargo})

#endregion

#region PRODUCTOS

def insertarproducto(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    if request.method == "POST":
        if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('precio') and request.POST.get('cantidad'):
            productos = Producto()
            productos.nombre = request.POST.get('nombre')
            productos.descripcion = request.POST.get('descripcion')
            productos.precio = request.POST.get('precio')    
            productos.cantidad = request.POST.get('cantidad')
            productos.foto_url = request.FILES['foto_url']
            imagen = FileSystemStorage()
            imagen.save(productos.foto_url.name,productos.foto_url)
            productos.save()
            return redirect('/Producto/listado')
    return render(request, 'Producto/insertar.html')

def listadoproducto(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    productos= Producto.objects.all()
    return render(request, 'Producto/listar.html', {'productos': productos})

def productoactualizar(request, id):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        cantidad = request.POST.get('cantidad')
        foto_url = request.FILES.get('foto_url')
        
        if nombre and descripcion and precio and cantidad:
            productos = Producto.objects.get(id=id)
            productos.nombre = nombre
            productos.descripcion = descripcion
            productos.precio = precio
            productos.cantidad = cantidad
            if 'foto_url' in request.FILES:
                productos.foto_url = request.FILES['foto_url']
            
            if foto_url:
                imagen = FileSystemStorage()
                filename = imagen.save(foto_url.name, foto_url)
                productos.foto_url = filename
            
            productos.save()
            return redirect('/Producto/listado/')
    
    else:
        productos = Producto.objects.get(id=id)
        return render(request, "Producto/actualizar.html", {"productos": productos})
    
def borrarproducto(request, id):
    productos = Producto.objects.filter(id=id)
    productos.delete()
    return redirect('/Producto/listado')

#endregion

#region FACTURA

def facturainsertar(request):
    if not request.user.is_authenticated:
        return redirect("/Usuarios/login")
    
    if request.method == "POST":
        if request.POST.get('idcliente') and request.POST.get('fechafactura') and request.POST.get('idproductoinput[]') and request.POST.get('cantidadproductoinput[]') and request.POST.get('totalfacturainput'):
            factura = Factura()
            factura.fecha = request.POST.get('fechafactura')
            factura.total = request.POST.get('totalfacturainput')
            factura.cliente = Clientes.objects.get(id=request.POST.get('idcliente'))
            factura.save()
    else:
        productos = Producto.objects.all()
        return render(request, 'Factura/insertar.html', {'productos': productos})

#endregion

#region USUARIOS

def insertarusuario(request):
    if request.method == "POST":
        if request.POST.get('nombres') and request.POST.get('apellidos') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password'):
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            user.first_name = request.POST.get('nombres')
            user.last_name = request.POST.get('apellidos')
            user.save()
            return redirect('/Usuarios/login')
            
    return render(request, 'Usuarios/insertar.html')

def loginusuarios(request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('password'):
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                mensaje = "Usuario o Contraseña incorrectos, Intente de nuevo"
                return render(request, 'Usuarios/login.html', {'mensaje':mensaje})
    else:
        return render(request, 'Usuarios/login.html')
    
def logoutusuarios(request):
    logout(request)
    return redirect('/Usuarios/login')

#endregion