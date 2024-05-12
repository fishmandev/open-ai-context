from django.urls import path

from . import views

app_name = "dialogs"
urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("create", views.CreateView.as_view(), name="create"),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
