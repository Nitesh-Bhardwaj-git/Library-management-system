from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Book(models.Model):
    title  = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    category = models.CharField(max_length=150, blank=True, null=True)
    publication_year = models.CharField(max_length=4, blank=True, null=True)
    copies_total     = models.IntegerField(default=3)
    copies_available = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name    = models.CharField(max_length=200)
    email   = models.EmailField(unique=True)
    phone   = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    STATUS_CHOICES = [("borrowed", "Borrowed"), ("returned", "Returned")]

    book        = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    member      = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    loan_date   = models.DateField(default=timezone.now)
    due_date    = models.DateField(max_length=10)
    return_date = models.DateField(default=timezone.now)
    status      = models.CharField(default="borrowed", max_length=10, choices=STATUS_CHOICES,)

    def __str__(self):
        return f"{self.book} → {self.member}"


class Fine(models.Model):
    loan   = models.OneToOneField(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid   = models.BooleanField(default=False)

    FINE_PER_DAY = 20  

    def calculate_fine(self):
        if self.loan and self.loan.return_date and self.loan.due_date:
            late_days = (self.loan.return_date - self.loan.due_date).days
            return max(late_days, 0) * self.FINE_PER_DAY
        return 0

    def save(self, *args, **kwargs):
        self.amount = self.calculate_fine()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.loan:
            return f"{self.amount} for {self.loan}"
        else:
            return f"{self.amount} for {self.member}"

