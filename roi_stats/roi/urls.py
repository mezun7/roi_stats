from django.urls import path, include

from roi import views

app_name = 'roi'

urlpatterns = [
    path('', views.main, name='main'),

]