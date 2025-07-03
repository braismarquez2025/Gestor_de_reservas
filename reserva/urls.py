from django.urls import path
from gestor_reservas.views import ReservaCreateView, mostrar_reservas, reservas_api
from reserva.views import MisReservasListView, ReservaUpdateView, ReservaDeleteView



app_name = "reserva"

urlpatterns = [
    path('all/', mostrar_reservas, name='mostrar_reservas'),
    path('api/reservas/', reservas_api, name='reservas_api'),
    path("<int:year>/<int:month>/<int:day>/nueva/", ReservaCreateView.as_view(), name="crear_reserva"),
    path('mis-reservas/', MisReservasListView.as_view(), name='mis_reservas'),
    path('update/<pk>/', ReservaUpdateView.as_view(), name='reserva_update'),
    path('delete/<pk>/', ReservaDeleteView.as_view(), name='reserva_delete'),
]
