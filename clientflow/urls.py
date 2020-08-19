"""XXX_PROJECT_NAME_XXX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin, auth
from django.urls import path, include
from django.views.generic import TemplateView
from clientflow.app.forms import CustomAuthForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from clientflow.app.views import IndexView

handler404 = 'clientflow.app.views.handler404'
handler404 = 'clientflow.app.views.handler404'
urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('trocarsenha/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('trocarsenha/done', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('esqueciminhasenha/', auth_views.PasswordResetView.as_view(html_email_template_name='registration/boas-vindas.html') ,name='password_reset'),
    path('esqueciminha/done', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('novasenha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('novasenha/done', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('',  IndexView, name='index'),
    path('', include('clientflow.app.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),


]
