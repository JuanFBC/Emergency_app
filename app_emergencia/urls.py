"""
URL configuration for app_emergencia project.

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


from app import views

urlpatterns = [
    path('', views.inicio, name="login"),
    path('menu', views.menu, name="menu"),
    path('menu/perfil', views.perfil, name="menu/perfil"),
    path('menu/Emergencia', views.emergencia, name="menu/Emergencia"),
    path('colaborador<str:id>', views.colaborador, name="colaborador"),
    path('menu/Emergencia/crear_alerta', views.crear_alerta, name=""),
    path('volver', views.regresar, name="volver"),
    path('menu/volver_menu', views.regresar_menu, name="menu_volver"),
    path('menu/Emergencia/crear_alertas', views.crear_alertas, name="menu/Emergencia/crear_alertas"),
    path('cerrar_alertas/<str:id>', views.cerrar_alertas, name="cerrar_alertas"),
    path('menu/crear_estado', views.crear_estado, name="menu/crear_estado"),
    path('menu/crear_estados', views.crear_estados, name="menu/crear_estados"),
    path('colaboradorver/<str:id>', views.colaborador_perfil, name="colaboradorver"),
    path('buscar', views.buscar_colaborador, name="Buscar"),
    path('menu/aud', views.aut, name="menu/aud")
]

