from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'), # Home page 
    path('black_list/', views.black_list, name='black_list'), # Black list page
]