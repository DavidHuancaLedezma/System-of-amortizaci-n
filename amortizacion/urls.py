from django.urls import path
from . import views
urlpatterns = [
    path("", views.seleccion_problema, name="seleccion_problema"),
    path("home/", views.home,name="home"),
    path("sac/", views.sac,name="sac"),
    path("resultados_sac/", views.resultados_sac, name="resultados_sac"),
    path("resultados_price/", views.resultados_price, name="resultados_price"),
    path("manual_de_uso/", views.manual_de_uso, name="manual_de_uso")
]