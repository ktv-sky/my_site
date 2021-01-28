from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='blog/', permanent=True)),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
]
