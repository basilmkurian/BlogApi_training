from rest_framework import serializers
from .models import Blog, Author, Category
from django.contrib.auth import get_user_model

class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'category', 'is_published']


Author = get_user_model()

class AuthorCreateSerializer(serializers.ModelSerializer):
    num_blogs = serializers.IntegerField(read_only=True)
    class Meta:
        model = Author
        fields = ['username', 'password', 'bio', 'contact_info', 'num_blogs']

    def get_num_blogs(self, obj):
        # Return the count of blogs associated with the author
        return obj.blog_set.count()

    def create(self, validated_data):
        # Handle password securely
        password = validated_data.pop('password')
        author = Author(**validated_data)
        author.set_password(password)
        author.save()
        return author

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'category', 'is_published', 'publish_date']
        read_only_fields = ['publish_date']


class AuthorSerializer(serializers.ModelSerializer):
    num_posts = serializers.IntegerField()

    class Meta:
        model = Author
        fields = ['username', 'num_posts']

class CategorySerializer(serializers.ModelSerializer):
    num_blogs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'num_blogs']  # Include num_blogs in fields

    def get_num_blogs(self, obj):
        return Blog.objects.filter(category=obj).count()
