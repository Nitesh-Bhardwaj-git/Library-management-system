from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone as dj_timezone
from django.db import transaction


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
    due_date    = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status      = models.CharField(default="borrowed", max_length=10, choices=STATUS_CHOICES,)

    def __str__(self):
        return f"{self.book} → {self.member}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        previous_instance = None
        if not is_new:
            try:
                previous_instance = Loan.objects.select_related('book').only('book_id', 'status', 'return_date').get(pk=self.pk)
            except Loan.DoesNotExist:
                previous_instance = None

        # Auto-derive status from return_date when appropriate (only on updates)
        if not is_new and self.return_date and self.status == 'borrowed':
            self.status = 'returned'

        super().save(*args, **kwargs)

        # Adjust stock after saving to ensure book relation exists
        if is_new:
            if self.status == 'borrowed' and self.book:
                if self.book.copies_available > 0:
                    self.book.copies_available -= 1
                    self.book.save(update_fields=['copies_available'])
        else:
            # Handle transitions and book changes
            if previous_instance:
                previous_book = previous_instance.book
                current_book = self.book
                prev_status = previous_instance.status
                curr_status = self.status

                # If book changed while still borrowed, return to previous and borrow from current
                if previous_book and current_book and previous_book != current_book:
                    if prev_status == 'borrowed':
                        previous_book.copies_available += 1
                        previous_book.save(update_fields=['copies_available'])
                    if curr_status == 'borrowed' and current_book.copies_available > 0:
                        current_book.copies_available -= 1
                        current_book.save(update_fields=['copies_available'])
                else:
                    # Same book: handle status transitions
                    if previous_book:
                        if prev_status == 'borrowed' and curr_status == 'returned':
                            previous_book.copies_available += 1
                            previous_book.save(update_fields=['copies_available'])
                            # Delete any fine associated with this loan upon return
                            from .models import Fine  # local import to avoid circular at import time
                            Fine.objects.filter(loan=self).delete()
                        elif prev_status == 'returned' and curr_status == 'borrowed':
                            if previous_book.copies_available > 0:
                                previous_book.copies_available -= 1
                                previous_book.save(update_fields=['copies_available'])

        # Ensure an overdue fine exists/updates when loan is overdue and still borrowed
        if self.status == 'borrowed' and self.due_date and self.due_date < dj_timezone.localdate():
            from .models import Fine  # local import to avoid circular reference at import time
            fine, _ = Fine.objects.get_or_create(loan=self, defaults={'member': self.member, 'amount': 0})
            fine.member = self.member
            fine.amount = fine.calculate_fine()
            fine.paid = False
            fine.save(update_fields=['member', 'amount', 'paid'])

    def delete(self, *args, **kwargs):
        # If a borrowed loan is deleted, return the copy to stock
        if self.book and self.status == 'borrowed':
            self.book.copies_available += 1
            self.book.save(update_fields=['copies_available'])
        # Delete associated fine for this loan
        from .models import Fine  # local import to avoid circular at import time
        Fine.objects.filter(loan=self).delete()
        super().delete(*args, **kwargs)


class Fine(models.Model):
    loan   = models.OneToOneField(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid   = models.BooleanField(default=False)

    FINE_PER_DAY = 20  

    def calculate_fine(self):
        if self.loan and self.loan.due_date:
            # If returned, compute based on return_date; otherwise compute up to today
            if self.loan.return_date:
                late_days = (self.loan.return_date - self.loan.due_date).days
            else:
                today = dj_timezone.localdate()
                late_days = (today - self.loan.due_date).days
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

