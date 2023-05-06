from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Genre, Category, Title, Review, Comment
from user.models import User


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        avg = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return avg['score__avg']


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

        def validate_year(self, value):
            year_now = timezone.now.year
            if value <= 0 or value > year_now:
                raise serializers.ValidationError(
                    'Год создания записи не должен превышать текущий.'
                )
            return value


class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор для модели Review."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )
    score = serializers.IntegerField(
        required=True,
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1))
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if request.method == 'POST':
            if title.reviews.filter(title=title_id, author=author).exists():
                raise ValidationError('Один отзыв на произведение!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Серилизатор для модели Comment."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Comment
        read_only_fields = ('author', 'review')
        exclude = ('review',)
