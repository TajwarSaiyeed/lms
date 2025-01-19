from django.contrib import admin

from .models import BookCategory, Book, BookBorrowing, Review

admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(BookBorrowing)
admin.site.register(Review)