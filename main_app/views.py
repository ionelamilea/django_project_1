import json
from http.client import responses

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated

from .forms import BookForm
from .models import Book,Pizza
from .serializers import BookSerializer, HWDataSerializer, PizzaSerializer
from rest_framework import viewsets
from rest_framework.response import Response

@login_required
def my_books(request):
    books = request.user.books.all()
    return render(request, 'my_books.html', {'books':books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            return HttpResponse("Book added successfully!")
    else:
        form = BookForm()
        return render(request, 'add_book.html', {'form':form})

@login_required()
def delete_book(request,book_id):
    book = get_object_or_404(Book, id=book_id, created_by=request.user)
    if request.method == "POST":
        book.delete()
        return redirect("my_books")

@login_required()
def confirm_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id, created_by=request.user)
    return render(request, 'confirm_delete.html', {'book':book})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookCustomViewSet(viewsets.ViewSet):

    # HTTP GET localhost:8000/custom_books/
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    # HTTP GET localhost:8000/custom_books/1/
    def retrieve(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found!"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # HTTP POST localhost:8000/custom_books/
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"message": "book deleted successfully!"}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found!"}, status=status.HTTP_404_NOT_FOUND)


class ActionViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = HWDataSerializer(data=request.data)
        result = []
        if serializer.is_valid():
            print(serializer.validated_data)
            first_list = serializer.validated_data['first_list']
            second_list = serializer.validated_data['second_list']

            for l in first_list:
                if l in second_list:
                    result.append(l)
            return Response({"result": result}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


content = [
    "Samsung galaxy 1",
    "Sony Xperia 5",
    "iPhone 14",
    "AllView 3"
]

books = ["1984", "To Kill a Mockingbird", "The Great Gatsby", "Moby-Dick", "Pride and Prejudice"]

# Create your views here.

def home(request):
    # return HttpResponse(content)
    # return redirect("https://google.com/")
    return render(request, 'home.html', {
        "content": content
    })


def second(request):
    return render(request, 'second.html')


def get_data(request: HttpRequest):
    return HttpResponse(json.dumps(content))


def get_books_page(request):
    return render(request, 'books.html', {
        "book_titles": books
    })


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def get_books(request: HttpRequest):
    if request.method == "GET":
        return HttpResponse(json.dumps(books))
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            books.append(data['book_title'])
            return HttpResponse("Book Added!", status=201)
        except Exception as e:
            return HttpResponse(str(e), status=400)
    elif request.method == "DELETE":
        books.clear()
        return HttpResponse(json.dumps(books), status=200)
    elif request.method == "PUT":
        data = json.loads(request.body)
        id = int(data['id'])
        title = data['book_title']
        if id >= 0 and not id > len(books) - 1:
            books[id] = title
            return HttpResponse(json.dumps(books[id]), status=200)
        else:
            return HttpResponse("Wrong ID given!", status=400)



class PizzaCustomViewSet(viewsets.ViewSet):
    # HTTP GET localhost:8000/custom_pizzas/
    def list(self,request):
        pizza = Pizza.objects.all()
        serializer = PizzaSerializer(pizza, many=True)
        return Response(serializer.data)

    # HTTP GET localhost:8000/custom_pizzas/1/
    def retrieve(self,request, pk=None):
        try:
            pizza = Pizza.objects.get(pk=pk)
            serializer = PizzaSerializer(pizza)
            return Response(serializer.data)
        except Pizza.DoesNotExist:
            return Response({"error": "Pizza not found!"}, status=status.HTTP_404_NOT_FOUND)

    # HTTP POST localhost:8000/custom_pizzas/
    def create(self,request):
        serializer = PizzaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        try:
            pizza = Pizza.objects.get(pk=pk)
            pizza.delete()
            return Response({"message": "pizza deleted successfully"}, status=status.HTTP_200_OK)
        except Pizza.DoesNotExist:
            return Response({"error": "Pizza not found"}, status = status.HTTP_404_NOT_FOUNDH)


















from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


# class BookCustomViewSet(viewsets.ViewSet):
#
#     def list(self, request):
#         """ GET: List all books """
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         """ GET: Retrieve a specific book by ID """
#         try:
#             book = Book.objects.get(pk=pk)
#             serializer = BookSerializer(book)
#             return Response(serializer.data)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def create(self, request):
#         """ POST: Create a new book """
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def update(self, request, pk=None):
#         """ PUT: Update a book (full update) """
#         try:
#             book = Book.objects.get(pk=pk)
#             serializer = BookSerializer(book, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def partial_update(self, request, pk=None):
#         """ PATCH: Partially update a book """
#         try:
#             book = Book.objects.get(pk=pk)
#             serializer = BookSerializer(book, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     def destroy(self, request, pk=None):
#         """ DELETE: Remove a book """
#         try:
#             book = Book.objects.get(pk=pk)
#             book.delete()
#             return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#


