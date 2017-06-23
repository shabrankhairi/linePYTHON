from django.conf.urls import url
from linefix import views

urlpatterns = [
               url(r'^callback$', views.callback, name='callback'),
               ]