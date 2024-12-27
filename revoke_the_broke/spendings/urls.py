from django.urls import path
from . import views


urlpatterns = [
    path('<int:id>/', views.category_spendings, name='category_spendings'),
    path('add/<int:category_id>/', views.add_expenditure, name='add_expenditure'),
    path('update/<int:category_id>/<int:exp_id>/', views.update_expenditure, name='edit_expenditure'),
    path('delete/<int:category_id>/<int:exp_id>/', views.delete_expenditure, name='delete_expenditure'),
]