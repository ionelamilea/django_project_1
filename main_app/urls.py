from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import BookViewSet, BookCustomViewSet, ActionViewSet, PizzaCustomViewSet

router = DefaultRouter()
router.register('books_api', BookViewSet, basename='book')
router.register('custom_books', BookCustomViewSet, basename="custom_book")
router.register('common_elements', ActionViewSet, basename="common_elements")
router.register('custom_pizza', PizzaCustomViewSet, basename="custom_pizza")

urlpatterns = [
    # path("", views.home, name="home"),
    # path("second", views.second, name="second"),
    # path("get_data", views.get_data, name="get_data"),
    # path("api/books", views.get_books, name="get_books"),
    # path("books", views.get_books_page, name="books_page")
    path("", include(router.urls)),
    path("home/", views.home, name="home"),
    path('books/add/', views.add_book, name='add_book'),
    path('books/', views.my_books, name='my_books'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'), #books/delete/2/
    path('books/conform_delete/<int:book_id>/', views.confirm_delete, name='confirm_delete')  # books/delete/2/

]

