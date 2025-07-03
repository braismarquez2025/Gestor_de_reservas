from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
from .models import Reserva
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
class ReservaListView(ListView):
    model = Reserva
    template_name = "reservas/mostrar_reservas.html"
    context_object_name = "reservas"

    def get_queryset(self):
        return Reserva.objects.all()
    

class MisReservasListView(ListView):
    model = Reserva
    template_name = "reservas/mis_reservas.html"
    context_object_name = "reservas"

    def get_queryset(self):
        return Reserva.objects.filter(user = self.request.user)
    


class ReservaUpdateView(UpdateView):
    model = Reserva
    template_name = "reservas/reserva_update.html"
    context_object_name = "reserva" 
    fields = ['fecha_hora', 'recurso']
    success_url = reverse_lazy('reserva:mis_reservas')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Reserva editada correctamente")
        return super(ReservaUpdateView, self).form_valid(form)
    


class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = "reservas/reserva_delete.html"
    context_object_name = "reserva"
    success_url = reverse_lazy('reserva:mis_reservas')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Reserva cancelada correctamente")
        return super(ReservaDeleteView, self).form_valid(form)



