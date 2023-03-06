from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import workers
from settings import settings
from workers.views import Workers_Login, Workers_Logout, error_noAccess_403

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('workers.urls')),
    path('', include('workers_certificates.urls')),
    path('', include('workers_planning.urls')),
    path('', include('projects.urls')),

    path('login/', Workers_Login.as_view(), name='login'),
    path('logout/', Workers_Logout.as_view(), name='logout'),

]
# обработчик для 404. Страница не найдена
# handler404 = error_pageNotFound_404
# ошибка сервера
# handler500 = error_errorServer_500
# доступ запрещен
handler403 = error_noAccess_403
# невозможно обработать запрос
# handler400 = error_error_400

# Все пользователи
# Страничка одного пользователя
# Добавить нового пользователя
# включаем возможность обработки картинок
# включаем возможность обработки картинок
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
