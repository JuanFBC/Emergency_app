from urllib import request
import requests
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from app.models import Colaborador
import socket
import nmap

def inicio(request):
    auditar(request)
    return render(request, "index.html")







def menu(request):
    auditar(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        pws = request.POST.get('password')
        user = consulta("SELECT contrasena, cedula, rol FROM app_administrador WHERE correo = '" + username +"'")
        if user:
            if user[0][0] == pws:
                request.session['username'] = username
                request.session['id'] = user[0][1]
                request.session['rol'] = user[0][2]
                
                


    
    if request.session.get('username', None):
        auditar(request)
        seg  = consulta("SELECT c.nombre, c.localidad, c.estado, s.fecha_hora FROM public.app_colaborador AS c JOIN public.app_seguimiento AS s ON c.id = s.id_colaborador_id ORDER BY s.fecha_hora DESC LIMIT 3;")
        return render(request, "menu.html", {"seguimiento": seg, "user": request.session['rol']})
     
    return redirect('/')













def colaborador_perfil(request,id):
    auditar(request)
        
        
        
    if request.session.get('username', None):
        
        if request.method == 'POST':
            id = request.POST.get('ids')
            estado = request.POST.get('estado')
            localidad = consulta("SELECT localidad FROM public.app_colaborador WHERE id = "+id+"")
            emerg = consulta("SELECT id FROM public.app_emergencia WHERE localidad = '"+str(localidad[0][0])+"' AND act = true;")
            sql = "INSERT INTO public.app_seguimiento(id_colaborador_id, id_emergencia_id, fecha_hora)VALUES ('"+str(id)+"', '"+(str)(emerg[0][0])+"', '"+(str)(timezone.now())+"');"
            insertar(sql)
            insertar("UPDATE public.app_colaborador SET estado='"+estado+"' WHERE id ='"+str(id)+"';")
            redirect('colaborador/0')
        
        cola = consulta("SELECT c.nombre,c.localidad,c.estado, s.fecha_hora AS ultima_actualizacion, C.id FROM  public.app_colaborador c JOIN public.app_seguimiento s ON c.id = s.id_colaborador_id WHERE c.id="+id+" AND s.fecha_hora = (SELECT MAX(s2.fecha_hora) FROM public.app_seguimiento s2 WHERE s2.id_colaborador_id = c.id);")
        
        return render(request, "colaborador.html", {"cola": cola})
    
    return redirect('/')




def perfil(request):
    auditar(request)
    if request.session.get('username', None):
        admin = consulta("SELECT cedula,nombre, numero, correo FROM app_administrador WHERE correo = '" + request.session['username'] +"'")

        return render(request, "perfil.html", {"admin": admin})
    return redirect('/')


def emergencia(request):
    auditar(request)
    
    if request.session.get('username', None):
        alertas = consulta("SELECT e.id, c.localidad, COUNT(c.id) AS total_colaboradores, SUM(CASE WHEN c.estado = TRUE THEN 1 ELSE 0 END) AS colaboradores_a_salvo, SUM(CASE WHEN c.estado = FALSE THEN 1 ELSE 0 END) AS colaboradores_comprometidos FROM public.app_colaborador c JOIN public.app_emergencia e ON c.localidad = e.localidad AND e.act = TRUE GROUP BY e.id, c.localidad;")
        return render(request, "lista_alertas.html", {"alertas": alertas})
    return redirect('/')


def colaborador(request,id):
    auditar(request)

    if request.session.get('username', None):
        
        if id == "0":
            seg = consulta("SELECT c.nombre,c.localidad,c.estado, s.fecha_hora AS ultima_actualizacion, c.id, c.numero FROM  public.app_colaborador c JOIN public.app_seguimiento s ON c.id = s.id_colaborador_id WHERE s.fecha_hora = (SELECT MAX(s2.fecha_hora) FROM public.app_seguimiento s2 WHERE s2.id_colaborador_id = c.id);")
            
        if id != "0":
            seg  = consulta("SELECT c.nombre, c.localidad, c.estado, s.fecha_hora, c.id, c.numero FROM public.app_colaborador AS c JOIN public.app_seguimiento AS s ON c.id = s.id_colaborador_id AND s.id_emergencia_id ="+id+" ORDER BY s.fecha_hora DESC;")
        nombres = Colaborador.objects.values_list('nombre', flat=True)
        numero = [col[5] for col in seg]
        return render(request, "lista_colaboradores.html",{"colab": seg , "id":id, "nombres": nombres, "numero": numero})
    return redirect('/')


def crear_alerta(request):
    auditar(request)
    
    if request.session.get('username', None):
        seg = consulta("SELECT * FROM public.app_localidad ORDER BY id ASC ")
        return render(request, "crear_alerta.html",{"local": seg})
    return redirect('/')


def regresar(request):
    auditar(request)
    if request.session.get('username', None):
        return redirect('menu/Emergencia')
    return redirect('/')


def regresar_menu(request):
    auditar(request)
    if request.session.get('username', None):
        return redirect('menu')
    return redirect('/')




def crear_alertas(request):
    auditar(request)
    if request.session.get('username', None):
        if request.method == 'POST':
            localidad = request.POST.get('localidad')
            tipo = request.POST.get('tipo-emergencia') 
            fecha_actual = timezone.now()
            emerg = consulta("SELECT id FROM public.app_emergencia WHERE localidad = '"+localidad+"' AND act = true;")
            if not emerg:
                sql = "INSERT INTO public.app_emergencia (localidad, tipo, id_administrador_id, fecha, act) VALUES ( '"+localidad+"', '"+tipo+"', "+(str) (request.session['id'])+", '"+(str)(fecha_actual)+"', True);"
                insertar(sql)
                return redirect('menu/Emergencia')
            else:
                messages.error(request, 'No se puede crear la alerta en la localidad '+localidad+', Ya existe una en curso')
                return render(request, "crear_alerta.html")
    return redirect('/')



def cerrar_alertas(request,id):
    auditar(request)
    if request.session.get('username', None):
        sql = "UPDATE public.app_emergencia SET act = False WHERE id ="+id+";"
        insertar(sql)
        return redirect('menu/Emergencia')
    return redirect('/')






def crear_estado(request):
    auditar(request)
    if request.session.get('username', None):
        sql = "SELECT id,nombre,localidad FROM public.app_colaborador"
        user =  consulta(sql)
        return render(request, "crear_estado.html", {"user": user})
    return redirect('/')
     




def crear_estados(request):
    auditar(request)
    if request.session.get('username', None):

        if request.method == 'POST':
            colaborador = request.POST.get('id')
            estado = request.POST.get('estado')
            localidad = consulta("SELECT localidad FROM public.app_colaborador WHERE id = "+colaborador+"")
            emerg = consulta("SELECT id FROM public.app_emergencia WHERE localidad = '"+str(localidad[0][0])+"' AND act = true;")
            sql = "INSERT INTO public.app_seguimiento(id_colaborador_id, id_emergencia_id, fecha_hora, estado)VALUES ('"+colaborador+"', '"+(str)(emerg[0][0])+"', '"+(str)(timezone.now())+"', '"+estado+"');"
            insertar(sql)
            insertar("UPDATE public.app_colaborador SET estado='"+estado+"' WHERE id ='"+colaborador+"';")
            return redirect('menu')
        return redirect('menu/Emergencia')
    return redirect('/')


def buscar_colaborador(request):
    auditar(request)
    if request.session.get('username', None):
    
            
            
            
        if request.method == 'POST':
            id = "0"
            numero = request.POST.get('numero')
            nombre = request.POST.get('nombre')
            
            
            if id == "0":
                if nombre == "" and numero != "" :
                    seg = consulta("SELECT c.nombre,c.localidad,s.estado, s.fecha_hora AS ultima_actualizacion, c.id, c.numero FROM  public.app_colaborador c JOIN public.app_seguimiento s ON c.id = s.id_colaborador_id WHERE CAST(c.numero AS TEXT) LIKE '"+numero+"%' AND s.fecha_hora = (SELECT MAX(s2.fecha_hora) FROM public.app_seguimiento s2 WHERE s2.id_colaborador_id = c.id);")
                if nombre != "" and numero == "":
                    seg = consulta("SELECT c.nombre,c.localidad,s.estado, s.fecha_hora AS ultima_actualizacion, c.id, c.numero FROM  public.app_colaborador c JOIN public.app_seguimiento s ON c.id = s.id_colaborador_id WHERE c.nombre LIKE '"+nombre+"%' AND s.fecha_hora = (SELECT MAX(s2.fecha_hora) FROM public.app_seguimiento s2 WHERE s2.id_colaborador_id = c.id);")

                    
                if nombre == "" and numero== "":
                    seg = consulta("SELECT c.nombre,c.localidad,s.estado, s.fecha_hora AS ultima_actualizacion, c.id, c.numero FROM  public.app_colaborador c JOIN public.app_seguimiento s ON c.id = s.id_colaborador_id WHERE s.fecha_hora = (SELECT MAX(s2.fecha_hora) FROM public.app_seguimiento s2 WHERE s2.id_colaborador_id = c.id);")
                    
                    
            if id != "0":
                seg  = consulta("SELECT c.nombre, c.localidad, s.estado, s.fecha_hora, c.id, c.numero FROM public.app_colaborador AS c JOIN public.app_seguimiento AS s ON c.id = s.id_colaborador_id AND s.id_emergencia_id ="+id+" ORDER BY s.fecha_hora DESC;")
            nombres = Colaborador.objects.values_list('nombre', flat=True)
            numero = [col[5] for col in seg]
            return render(request, "lista_colaboradores.html",{"colab": seg , "id":id, "nombres": nombres, "numero": numero})
    return redirect('/')




def aut (request):
    if request.session.get('username', None):
    
        val = consulta("SELECT * FROM public.app_auditoria ORDER BY id DESC ")
                
        return render(request, "aut.html", {"colab": val})
    return redirect('/')





#Funciones
def consulta(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return resultado
    
def insertar(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()
        
def auditar(request):
    if request.session.get('username'):
        username = request.session.get('username')  
    else:
        username = 'Ususario no registrado'
    pagina = request.path
    fecha = timezone.now()

    x_forwarded_for = request.META.get('X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO public.app_auditoria (users, pagina, fecha, id_serv) VALUES (%s, %s, %s,%s)",
            (username, pagina, fecha, ip) 
        )

    geo_data = obtener_geolocalizacion(ip)

    city = geo_data.get('city')
    region = geo_data.get('region')
    country = geo_data.get('country')




def obtener_geolocalizacion(ip):
    url = f'https://ipinfo.io/{ip}/json'
    response = requests.get(url)
    data = response.json()
    return data