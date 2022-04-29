# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('bookstore.accounts.urls')),
    path('profile/', include('bookstore.profiles.urls')),
    path('', include('bookstore.books.urls')),
    path('', include('bookstore.news.urls')),
    path('api/', include('bookstore.api.urls'))
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
