"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.BookListView.as_view(), name='book_list'),
    path('add-book/', v.AddBookView.as_view(), name='add_book'),
    path('edit-book/<int:pk>/', v.EditBookView.as_view(), name='edit_book'),
    path('delete-book/<int:pk>/', v.DeleteBookView.as_view(),
         name='delete_book'),
    path('import-books/', v.ImportBookView.as_view(), name='import_books'),
    path('api/', v.BookAPIView.as_view(), name='api_book_list'),
]
