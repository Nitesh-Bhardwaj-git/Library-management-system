from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from .models import Book, Member, Loan, Fine
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .forms import CustomUserRegistrationForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import os



class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class BookList(AdminOnlyMixin, ListView):
    model = Book
    template_name = "Book_app/list.html"
    context_object_name = "books"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_books'] = Book.objects.order_by('-id')[:5]
        context['recent_members'] = Member.objects.order_by('-id')[:5]
        context['recent_loans'] = Loan.objects.order_by('-id')[:5]
        context['recent_fines'] = Fine.objects.order_by('-id')[:5]
        return context
    

class BookFullList(AdminOnlyMixin, ListView):
    model = Book
    template_name = "Book_app/book_list.html"
    context_object_name = "books"

class MemberFullList(AdminOnlyMixin, ListView):
    model = Member
    template_name = "Book_app/member_list.html"
    context_object_name = "members"

class LoanFullList(AdminOnlyMixin, ListView):
    model = Loan
    template_name = "Book_app/loan_list.html"
    context_object_name = "loans"

class FineFullList(AdminOnlyMixin, ListView):
    model = Fine
    template_name = "Book_app/fine_list.html"
    context_object_name = "fines"


class MemberList(AdminOnlyMixin, ListView):
    model = Member
    template_name = "Book_app/list.html"
    context_object_name = "members"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['loans'] = Loan.objects.all()
        context['fines'] = Fine.objects.all()
        return context


class LoanList(AdminOnlyMixin, ListView):
    model = Loan
    template_name = "Book_app/list.html"
    context_object_name = "loans"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['members'] = Member.objects.all()
        context['fines'] = Fine.objects.all()
        return context


class FineList(AdminOnlyMixin, ListView):
    model = Fine
    template_name = "Book_app/list.html"
    context_object_name = "fines"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['members'] = Member.objects.all()
        context['loans'] = Loan.objects.all()
        return context


class MemberCreate(AdminOnlyMixin, CreateView):
    model = Member
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("member-list")


class BookCreate(AdminOnlyMixin, CreateView):
    model = Book
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("book-list")


class LoanCreate(AdminOnlyMixin, CreateView):
    model = Loan
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("loan-full-list")

    def form_valid(self, form): 
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            member = Member.objects.filter(user=self.request.user).first()
            if not member:
                raise PermissionDenied("No member profile found for this user.")
            form.instance.member = member
        return super().form_valid(form)


class FineCreate(AdminOnlyMixin, CreateView):
    model = Fine
    fields = "__all__"
    template_name = "Book_app/create.html"
    success_url = reverse_lazy("fine-full-list")


class BookUpdate(AdminOnlyMixin, UpdateView):
    model = Book
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("book-list")


class MemberUpdate(AdminOnlyMixin, UpdateView):
    model = Member
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("member-list")


class LoanUpdate(AdminOnlyMixin, UpdateView):
    model = Loan
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("loan-list")


class FineUpdate(AdminOnlyMixin, UpdateView):
    model = Fine
    fields = "__all__"
    template_name = "Book_app/update.html"
    success_url = reverse_lazy("fine-list")


class BookDelete(AdminOnlyMixin, DeleteView):
    model = Book
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("book-list")


class MemberDelete(AdminOnlyMixin, DeleteView):
    model = Member
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("member-list")


class LoanDelete(AdminOnlyMixin, DeleteView):
    model = Loan
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("loan-list")


class FineDelete(AdminOnlyMixin, DeleteView):
    model = Fine
    template_name = "Book_app/delete.html"
    success_url = reverse_lazy("fine-list")


class RegisterView(FormView):
    template_name = 'Book_app/register.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        Member.objects.create(user=user, name=user.username, email=user.email, phone=form.cleaned_data['phone'])
        return super().form_valid(form)


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Book_app/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.filter(user=self.request.user).first()
        context['member'] = member
        context['loans'] = Loan.objects.filter(member=member)
        context['fines'] = Fine.objects.filter(member=member)
        return context

class CustomLoginView(LoginView):
    template_name = 'Book_app/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return '/'  
        return '/dashboard/'


class CreateSuperuserView(TemplateView):
    template_name = 'Book_app/create_superuser.html'
    
    def get(self, request, *args, **kwargs):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        if not all([username, email, password]):
            return HttpResponse("Environment variables not set properly", status=400)
        
        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            return HttpResponse(f"Superuser '{username}' already exists")
        
        try:
            User.objects.create_superuser(username, email, password)
            return HttpResponse(f"Superuser '{username}' created successfully! You can now login.")
        except Exception as e:
            return HttpResponse(f"Error creating superuser: {e}", status=500)
