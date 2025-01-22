from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('expenses/',views.index,name='expenses'),
    path('add-expense/',views.add_expense,name='add-expenses'),
    path('edit-expense/<int:id>',views.edit_expenses,name='edit-expenses'),
    path('delete-expense/<int:id>',views.delete_expenses,name='delete-expenses'),
    path('search-expenses',csrf_exempt(views.search_expenses),name='search-expenses'),
    
    path('expense_category_summary',views.expense_category_summary,name='expense_category_summary'),
    path('stats',views.stats_view,name='stats'),
    
    path('export-csv',views.export_csv,name='export-csv'),
    path('export-excel',views.export_excel,name='export-excel'),
]
