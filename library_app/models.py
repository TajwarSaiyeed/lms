from django.db import models
from django.contrib.auth.models import User

class BookCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/')
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

class BookBorrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrower')
    borrowed_after_balance = models.DecimalField(max_digits=10, decimal_places=2)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return  f'{self.borrower.username} borrowed book "{self.book.title}" on date {self.borrowed_at.date()} with price of {self.book.borrowing_price} $'

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete = models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name='books')
    review_text= models.TextField(null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for book : {self.book.title}"