from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
import calendar
from datetime import datetime, date
from django.utils import timezone
from gestor_reservas.forms import LoginForm, RegistrationForm, ReservaForm
from recurso.models import Recurso
from reserva.models import Reserva
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from reserva.models import Reserva
import json
from django.views.decorators.csrf import csrf_exempt
from django.views import View



class HomeView(TemplateView):
    template_name = "general/home.html"



@csrf_exempt  # solo para pruebas, luego manejar CSRF con token
def reservas_api(request):
    if request.method == 'GET':
        reservas = Reserva.objects.select_related('user', 'recurso').all()
        data = []
        for r in reservas:
            data.append({
                'id': r.id,
                'title': f"{r.user.username if r.user else 'Sin usuario'} - {r.recurso.nombre if r.recurso else 'Sin recurso'}",
                'start': r.fecha_hora.isoformat(),
                'end': None,
            })
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            fecha_hora = data.get('fecha_hora')
            recurso_id = data.get('recurso_id')
            # Aquí deberías validar fecha_hora y recurso_id y crear la reserva
            # Ejemplo simple (ajusta según tu modelo y lógica):
            from django.contrib.auth.models import User
            user = request.user if request.user.is_authenticated else None

            from datetime import datetime
            fecha_hora_obj = datetime.fromisoformat(fecha_hora)
            fecha_hora_obj = timezone.make_aware(fecha_hora_obj, timezone.get_current_timezone())

            recurso = Recurso.objects.get(id=recurso_id)

            #Comprobamos que no exista ya una reserva ese dia a esa hora 
            existe = Reserva.objects.filter(
                fecha_hora=fecha_hora,
                recurso=recurso
            ).exists()

            if existe:
                return JsonResponse({
                'message': f"Ya existe una reserva, lo sentimos. Escoge un dia y una hora disponible"
            }, status=400)


            nueva_reserva = Reserva.objects.create(
                user=user,
                recurso=recurso,
                fecha_hora=fecha_hora_obj
            )


            return JsonResponse({
                'id': nueva_reserva.id,
                'title': f"{user.username if user else 'Sin usuario'} - {recurso.nombre}",
                'start': nueva_reserva.fecha_hora.isoformat(),
                'end': None,
                'message': f"Se ha creado la reserva correctamente a nombre de {request.user}"
            }, status=201)
        

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def calendario_view(request):
    recursos = Recurso.objects.all()
    return render(request, 'general/calendar.html', {'recursos': recursos})



def mostrar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, "reservas/mostrar_reservas.html", {"reservas": reservas})



class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/crear_reserva.html"
    success_url = reverse_lazy("calendario") 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["year"] = self.kwargs.get("year")
        context["month"] = self.kwargs.get("month")
        context["day"] = self.kwargs.get("day")

        return context
    
    def get_form_kwargs(self):
        """
        Pasa selected_date al formulario.
        """
        kwargs = super().get_form_kwargs()

        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        day = int(self.kwargs.get('day'))
        selected_date = datetime(year, month, day).date()

        kwargs['selected_date'] = selected_date
        return kwargs
    

    def form_valid(self, form):
        """
        Completa fecha + hora antes de guardar.
        """
        # Recupera la fecha seleccionada
        year = int(self.kwargs.get('year'))
        month = int(self.kwargs.get('month'))
        day = int(self.kwargs.get('day'))
        selected_date = datetime(year, month, day).date()
        

        # Obtén la hora ingresada en el formulario
        selected_date = form.selected_date
        hora = form.cleaned_data['hora']

        # Combina fecha + hora
        fecha_hora = datetime(
            year=selected_date.year,
            month=selected_date.month,
            day=selected_date.day,
            hour=hora.hour,
            minute=hora.minute,
        )

        # Asigna la fecha_hora al objeto reserva
        form.instance.fecha_hora = fecha_hora

        return super().form_valid(form)
    


class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Bienvenido de nuevo {user.username}")
            return HttpResponseRedirect(
                reverse("home")
            )
        
        else:
            messages.add_message(
                self.request, messages.ERROR, 'Usuario no válido o contraseña incorrecta')
            return super(LoginView, self).form_invalid(form)
        


class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy("login")
    form_class = RegistrationForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente")
        return super(RegisterView, self).form_valid(form)



class LegalView(TemplateView):
    template_name = "general/legal.html"


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado sesión correctamente")
    return HttpResponseRedirect(reverse('home'))
                
                