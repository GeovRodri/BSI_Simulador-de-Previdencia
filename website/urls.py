from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from website import views
from website.views import Simulacao, Aposentar, AposentadosList, AposentadosDelete

urlpatterns = [
    url(r'^login$', auth_views.LoginView.as_view(template_name='login.html')),
    url(r'^logout$', auth_views.LogoutView.as_view(template_name='login.html')),
    url(r'^aposentar$', login_required(Aposentar.as_view())),
    url(r'^listar$', login_required(AposentadosList.as_view()), name='listar'),
    url(r'^delete/(?P<pk>\d+)/$', login_required(AposentadosDelete.as_view())),
    url(r'^simular/(?P<key>\d+)$', views.updateAposentado),
    url('', login_required(Simulacao.as_view()))
]
