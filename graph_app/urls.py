from django.urls import path
from . import views
urlpatterns = [
    path('', views.index_view, name='index'),           
    path('perhitungan-graf-lintasan/', views.graph_view, name='graph_form'),
    path('contoh-penerapan/', views.penerapan_view, name='graph_form'),
    path('sumber-referensi/', views.reference_view, name='reference'),
]
