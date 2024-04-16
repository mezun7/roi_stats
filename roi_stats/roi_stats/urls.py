"""
URL configuration for roi_stats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from roi import views


urlpatterns = [
    path('', include(('roi.urls', 'roi'), namespace='roi')),
    path('olympiads/<int:pk>/results', views.olympiad_result, name='olympiad_results'),
    path('olympiads/<int:pk>', views.olympiad_result, name='olympiad_main'),
    path('olympiads/<int:olympiad_pk>/regions', views.regions_olymp_result, name='region_olympiad_results'),
    path('region/<int:region_pk>/', views.region_view, name='region'),
    path('region/<int:region_pk>/results', views.region_results_view, name='region_results'),
    path('region/<int:region_pk>/delegations', views.region_delegetaions_view, name='region_delegations'),
    path('student/<int:student_pk>', views.student_view, name='student_view'),
    path('region/<int:region_pk>/hall_of_fame', views.region_hall_of_fame, name='region_hall_of_fame'),
    path('halloffame', views.region_hall_of_fame, name='hall_of_fame'),
    path('regions', views.regions_results, name='regions_results'),
    path('test', views.fix_patranomic, name='fix_patronomic'),
    path('admin/', admin.site.urls),
]
