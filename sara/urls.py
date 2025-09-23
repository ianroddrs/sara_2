# --- Arquivo Principal de URLs: sara/urls.py ---
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Inclui as URLs do nosso app principal
    path('phoenix/', include('phoenix.urls')), # Adicione esta linha
]

# Adiciona URLs para servir arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)