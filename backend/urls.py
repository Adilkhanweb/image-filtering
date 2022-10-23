from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.ConverterView.as_view(), name="create"),
    path('', views.ConverterShowView, name="index"),
    path('<int:id>', views.ConverterDetailView.as_view(), name="detail"),
]
