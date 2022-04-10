from rest_framework.response import Response
from rest_framework.views import APIView

from bookstore.api.serializers import BookSerializer
from bookstore.books.models import Book


class ApiListBooksView(APIView):

    def get(self, request, pk):
        books = Book.objects.filter(author_id=pk)
        serializer = BookSerializer(books, many=True)
        return Response({"books": serializer.data})
