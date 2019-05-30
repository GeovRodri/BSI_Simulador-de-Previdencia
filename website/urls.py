from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from website.views import Simulacao

urlpatterns = [
    url(r'^login$', auth_views.LoginView.as_view(template_name='login.html')),
    url(r'^logout$', auth_views.LogoutView.as_view(template_name='login.html')),
    url('', login_required(Simulacao.as_view()))
]