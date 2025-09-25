from django.core.management.base import BaseCommand
from django.utils import timezone
from Book_app.models import Loan, Fine


class Command(BaseCommand):
    help = "Generate or update fines for overdue loans. Intended for daily scheduling."

    def handle(self, *args, **options):
        today = timezone.localdate()

        overdue_loans = Loan.objects.filter(status='borrowed', due_date__lt=today)

        created_count = 0
        updated_count = 0

        for loan in overdue_loans:
            fine, created = Fine.objects.get_or_create(loan=loan, defaults={'member': loan.member, 'amount': 0})
            previous_amount = fine.amount
            fine.member = loan.member
            fine.amount = fine.calculate_fine()
            fine.save(update_fields=['member', 'amount', 'paid'])
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Fines processed. Created: {created_count}, Updated: {updated_count}"
        ))


