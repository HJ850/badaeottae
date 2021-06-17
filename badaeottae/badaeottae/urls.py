"""badaeottae URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers
from bada import views

router=routers.DefaultRouter()
router.register('',views.TestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('bada/',include('bada.urls')),
    path('tests/',include(router.urls)),
    
    path('', views.home),
    path('beach_insert/', views.beach_insert),
    path('weather_insert/', views.weather_insert),
    path('pred_insert/', views.pred_insert),
    path('score_insert/', views.score_insert),
    path('jellyfish_insert/', views.jellyfish_insert),
    path('plankton_insert/', views.plankton_insert),
    
    path('table_list/', views.table_list),
    path('graph_list/', views.graph_list),
    
    path('weather_heatmap/', views.weather_heatmap),
    path('jf_clustering/', views.jf_clustering),
    path('plankton_heatmap/', views.plankton_heatmap),
    path('moak_nomura/', views.moak_nomura),
    path('chucksek_nomura/', views.chucksek_nomura),
]
