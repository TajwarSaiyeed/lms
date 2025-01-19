from django.utils import timezone
from library_app.models import BookCategory
from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = BookCategory.objects.all()
        context['categories'] = categories

        current_category_id = self.request.GET.get('category')
        if current_category_id:
            current_category = BookCategory.objects.filter(id=current_category_id).first()
            filtered_books = current_category.books.all() if current_category else []
            context.update({
                'current_category_id': current_category_id,
                'current_category_name': current_category.name if current_category else '',
                'filtered_books': filtered_books,
            })
        else:
            all_books_by_category = {
                category: category.books.all() for category in categories
            }
            context.update({
                'current_category_id': None,
                'all_books_by_category': all_books_by_category,
            })

        return context

def send_transaction_email(user, amount, mail_subject, template_name, extra_context=None):
    context = {
        'user': user,
        'amount': amount,
        'timestamp': timezone.now(),
        'app_name': "LMS",
        'year': timezone.now().year,
    }
    if extra_context:
        context.update(extra_context)

    message_body = render_to_string(template_name, context)

    email = EmailMultiAlternatives(
        mail_subject,
        '',
        '',
        [user.email],
    )
    email.attach_alternative(message_body, "text/html")
    email.send()
    return email
