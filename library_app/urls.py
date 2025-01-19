
from django.urls import path
from library_app.views import BorrowBookView, ReturnBookView, BookDetailView, ReviewBookView

urlpatterns = [
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:book_id>/borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('return-book/<int:pk>/', ReturnBookView.as_view(), name='return_book'),
    path('review-book/<int:pk>/', ReviewBookView.as_view(), name='add_review'),
]