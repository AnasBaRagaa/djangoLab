from django.urls import path
from . import views

app_name = 'phonebook'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('test/', views.CreateEntry.as_view(), name='create'),
    path('contact/', views.CreateContact.as_view(), name='create_contact'),
    path('entry/update/<int:pk>/', views.UpdateEntry.as_view(extra_context={'title':'Update Entry', 'ref': {'Contact': 'create_contact'}}), name='update'),
    path('entry/delete/<int:k>/', views.DeleteEntry.as_view(), name='delete'),
    path('contact/update/<int:pk>/', views.UpdateContact.as_view(extra_context={'title':'Update Contact', }), name='update_contact'),
    path('contact/delete/<int:pk>/', views.DeleteContact.as_view(), name='delete_contact')
]
