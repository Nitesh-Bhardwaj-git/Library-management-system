from django.urls import path
from . import views
from django.contrib.auth.views import  LogoutView
from .views import CustomLoginView, BookFullList, MemberFullList, LoanFullList, FineFullList

urlpatterns = [
    path('', views.BookList.as_view(), name="home"),
    
    # Temporary superuser creation - REMOVE AFTER USE
    path('create-superuser/', views.CreateSuperuserView.as_view(), name='create-superuser'),
    
    path('books/', views.BookList.as_view(), name="book-list"),
    path('book/create/', views.BookCreate.as_view(), name="book-create"),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name="book-update"),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name="book-delete"),
    path('books/all/', BookFullList.as_view(), name='book-full-list'),
    
   
    path('members/', views.MemberList.as_view(), name="member-list"),
    path('member/create/', views.MemberCreate.as_view(), name="member-create"), 
    path('member/<int:pk>/edit/', views.MemberUpdate.as_view(), name="member-update"),
    path('member/<int:pk>/delete/', views.MemberDelete.as_view(), name="member-delete"),
    path('members/all/', MemberFullList.as_view(), name='member-full-list'),
    
    
    path('loans/', views.LoanList.as_view(), name="loan-list"),
    path('loan/create/', views.LoanCreate.as_view(), name="loan-create"),
    path('loan/<int:pk>/edit/', views.LoanUpdate.as_view(), name="loan-update"),
    path('loan/<int:pk>/delete/', views.LoanDelete.as_view(), name="loan-delete"),
    path('loans/all/', LoanFullList.as_view(), name='loan-full-list'),
    
    
    path('fines/', views.FineList.as_view(), name="fine-list"),
    path('fine/create/', views.FineCreate.as_view(), name="fine-create"),
    path('fine/<int:pk>/edit/', views.FineUpdate.as_view(), name="fine-update"),
    path('fine/<int:pk>/delete/', views.FineDelete.as_view(), name="fine-delete"),
    path('fines/all/', FineFullList.as_view(), name='fine-full-list'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),

    
    
    
]

