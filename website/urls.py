from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from website.views import Simulacao, Aposentar, AposentadosList

urlpatterns = [
    url(r'^login$', auth_views.LoginView.as_view(template_name='login.html')),
    url(r'^logout$', auth_views.LogoutView.as_view(template_name='login.html')),
    url(r'^aposentar$', login_required(Aposentar.as_view())),
    url(r'^listar$', login_required(AposentadosList.as_view())),
    url('', login_required(Simulacao.as_view()))
]