from django.utils import timezone
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Genre, Category, Title, Review, Comment


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

    def get_rating(self, obj):
        avg = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return avg['score__avg']

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


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
    """Отзыв на произведение."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = ('id', 'title', 'author', 'pub_date', 'text', 'score')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        """Проверка, что отзыв не был напиан ранее."""

        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise serializers.ValidationError('Отзыв нельзя оставить дважды.')
        return data

    def validate_score(self, value):
        """Проверка поставленной оценки."""

        if 0 >= value >= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 0 до 10.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Комментарий к отзыву."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comment
