from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_user_post_limit(user):
    start_time = timezone.now() - timezone.timedelta(days=1)
    news_count = Post.objects.filter(author=user, created_at__gte=start_time).count()

    if news_count >= 3:
        raise ValidationError("Превышено ограничение на количество публикаций новостей.")


class Author(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    rating = IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        post_rating = sum(post.rating for post in self.posts.all())
        post_comments_rating = sum(
            comment.rating for post in self.posts.all() for comment in post.comments.all())
        personal_comments_rating = sum(
            comment.rating for comment in self.user.comments.all())
        self.rating = post_rating * 3 + post_comments_rating + personal_comments_rating
        self.save()


class Category(Model):
    name = CharField(max_length=255, unique=True)
    subscribers = ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return f'{self.name}'


class Post(Model):
    author = ForeignKey(Author, on_delete=CASCADE, related_name='posts', validators=[validate_user_post_limit])
    post_type_choices = [('article', 'Article'), ('news', 'News')]
    post_type = CharField(max_length=10, choices=post_type_choices)
    created_at = DateTimeField(auto_now_add=True)
    title = CharField(max_length=255)
    categories = ManyToManyField(Category, related_name='posts')
    content = TextField()
    rating = IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('news:post', kwargs={'pk': self.id})

    def __str__(self):
        return f"({self.get_post_type_display()} by {self.author.user.username}) {self.title}: {self.preview()}"

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Comment(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    user = ForeignKey(User, on_delete=CASCADE, related_name='comments')
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)
    rating = IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.text} ({self.created_at.strftime('%d %b %Y %H:%M')}) for {self.post.title}"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
