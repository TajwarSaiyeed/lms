
from django.contrib import admin
from django.urls import path, include

from LMS.views import HomeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    path('accounts/', include('user_app.urls')),
    path('transactions/', include('transactions.urls')),
    path('books/', include('library_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
