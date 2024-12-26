from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_category/', views.add_category, name='add_category'),
    path('update_category/<int:id>', views.update_category, name='update_category'),
    path('remove_category/<int:id>', views.remove_category, name='remove_category'),
]