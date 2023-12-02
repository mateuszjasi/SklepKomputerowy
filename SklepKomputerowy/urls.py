from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v.register, name="register"),
    path('', include("mainApp.urls")),
    path('', include("django.contrib.auth.urls")),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
