from django.db import connection
from django.shortcuts import redirect, render


def home(request):
    return render(request,'Home/home.html')

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
