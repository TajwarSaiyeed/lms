from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from LMS.views import send_transaction_email
from .models import Book, BookBorrowing, Review
from transactions.models import Transaction, REFUND



class BookDetailView(DetailView):
    model = Book
    template_name = 'book-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['book'] = book

        context['reviews'] = Review.objects.filter(book=book);

        if self.request.user.is_authenticated:
            context['is_borrowed'] = BookBorrowing.objects.filter(book=book, borrower=self.request.user, returned_at__isnull=True).exists()
            context['is_borrowed_by_user'] = BookBorrowing.objects.filter(book=book, borrower=self.request.user).exists()
        else:
            context['is_borrowed'] = False
            context['is_borrowed_by_user'] = False
        return context

class BorrowBookView(View):
    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        account = request.user.account

        if account.balance >= book.borrowing_price:
            account.balance -= book.borrowing_price
            account.save()

            Transaction.objects.create(
                amount=book.borrowing_price,
                balance_after_transaction=account.balance,
                account=account,
                    transaction_type='BORROW'
            )

            BookBorrowing.objects.create(
                book=book,
                borrower=request.user,
                borrowed_after_balance=account.balance
            )

            send_transaction_email(
                user=request.user,
                amount=book.borrowing_price,
                mail_subject=f"Borrowed Book Confirmation: {book.title}",
                template_name="borrow-book-email-template.html",
                extra_context={"book_title": book.title}
            )

            messages.success(request, f'You have successfully borrowed "{book.title}".')
        else:
            messages.error(request, 'Insufficient balance to borrow this book.')

        return redirect('book_detail', pk=book_id)


class ReturnBookView(View):
    def post(self, request, pk):
        book_borrowing = get_object_or_404(BookBorrowing, id=pk)
        book_borrowing.returned_at = timezone.now()
        book_borrowing.save()

        book = book_borrowing.book
        account = request.user.account
        account.balance += book.borrowing_price
        account.save()

        Transaction.objects.create(
            amount=book.borrowing_price,
            balance_after_transaction=account.balance,
            account=account,
            transaction_type=REFUND
        )

        send_transaction_email(
            user=request.user,
            amount=book.borrowing_price,
            mail_subject=f"Return Book Confirmation: {book.title}",
            template_name="return-book-email-template.html",
            extra_context={"book_title": book.title}
        )

        messages.success(request, f'You have successfully returned "{book.title}".')
        return redirect('profile')


class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        review_text = request.POST.get('review_text')
        is_borrowed = BookBorrowing.objects.filter(book=book, borrower=request.user).exists()

        if not is_borrowed:
            messages.error(request, f'You must borrow the book "{book.title}" before reviewing it.')
            return redirect('book_detail', pk=pk)

        Review.objects.create(
            reviewer=request.user,
            book=book,
            review_text=review_text
        )

        send_transaction_email(
            user=request.user,
            amount=None,
            mail_subject=f"Review Confirmation: {book.title}",
            template_name="review-book-email-template.html",
            extra_context={"book_title": book.title, "review_text": review_text}
        )

        messages.success(request, f'You have successfully reviewed "{book.title}".')
        return redirect('book_detail', pk=pk)

