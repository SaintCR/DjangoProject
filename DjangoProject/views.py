from django.db import connection
from django.shortcuts import redirect, render

from DjangoProject.models import Cargo, Clientes


def home(request):
    return render(request,'Home/home.html')

#region CLIENTES

def clienteinsertar(request):
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

#endregion

#region CARGO

def cargoinsertar(request):
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

