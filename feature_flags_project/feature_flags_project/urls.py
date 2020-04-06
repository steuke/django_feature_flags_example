from django.contrib import admin
from django.urls import path

from my_app.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view()),
]
