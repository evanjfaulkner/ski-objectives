from django.urls import path
from . import views

urlpatterns = [
    path('', views.ObjectiveListView.as_view(), name='objective-list'),
    path('objective/<int:pk>/', views.ObjectiveDetailView.as_view(), name='objective-detail'),
    path('objective/new/', views.ObjectiveCreateView.as_view(), name='objective-create'),
    path('objective/<int:pk>/edit/', views.ObjectiveUpdateView.as_view(), name='objective-update'),
    path('objective/<int:pk>/interest/', views.register_interest, name='register-interest'),
] 