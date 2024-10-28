from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError as DjangoValidationError
from rest_framework.response import Response
from .models import Blog, Author, Category
from .serializers import BlogCreateSerializer, AuthorCreateSerializer, BlogSerializer, AuthorSerializer, CategorySerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

Author = get_user_model()


class BlogCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            blog = serializer.save()

            if blog.is_published:
                message = "Blog post has been published successfully."
            else:
                message = "Blog post has been saved as a draft."

            return Response(
                {"message": message, "blog": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except DjangoValidationError as e:
            return Response(
                {"message": "Validation error occurred.", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "An error occurred.", "errors": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthorCreateAPIView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = AuthorCreateSerializer

class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# List all posts with title, author, and publish date
class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer

# List post and author details for each published post
class BlogDetailAPIView(generics.ListAPIView):
    def post(self, request):
        # Get the id from the JSON body
        blog_id = request.data.get('id')

        if not blog_id:
            return Response({"error": "ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the blog post
        blog = get_object_or_404(Blog, id=blog_id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Retrieve top 3 authors with the most posts in the last 6 months
class TopAuthorsAPIView(generics.ListAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        # Get top 3 authors with the most posts in the last 6 months
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        top_authors = Author.objects.annotate(
            num_posts=Count('blogs', filter=Q(blogs__publish_date__gte=six_months_ago))
        ).order_by('-num_posts')[:3]

        # Serialize the response
        author_data = [{"username": author.username, "num_posts": author.num_posts} for author in top_authors]

        return Response(author_data, status=status.HTTP_200_OK)

# Show the most popular category in the last 6 months
class PopularCategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get(self, request):
        # Get the most popular category in the last 6 months
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        
        # Annotate categories with the count of blogs published in the last 6 months
        popular_category = Category.objects.annotate(
            num_blogs=Count('blog', filter=Q(blog__publish_date__gte=six_months_ago))
        ).order_by('-num_blogs').first()  # Get the category with the most blogs
        
        if popular_category:
            category_data = {
                "name": popular_category.name,
                "description": popular_category.description,
                "num_blogs": popular_category.num_blogs
            }
            return Response(category_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No blogs found in the last 6 months."}, status=status.HTTP_404_NOT_FOUND)
        
class DraftListView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=False)  # Filter for drafts
    serializer_class = BlogSerializer  # Use the serializer to format the output

    def get(self, request, *args, **kwargs):
        drafts = self.get_queryset()
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)
