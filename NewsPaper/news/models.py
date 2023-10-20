from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse


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

    def __str__(self):
        return f'{self.name}'


class PostCategory(Model):
    post = ForeignKey('Post', on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)


class Post(Model):
    author = ForeignKey(Author, on_delete=CASCADE, related_name='posts')
    post_type_choices = [('article', 'Article'), ('news', 'News')]
    post_type = CharField(max_length=10, choices=post_type_choices)
    created_at = DateTimeField(auto_now_add=True)
    categories = ManyToManyField(Category, through=PostCategory, default=[])
    title = CharField(max_length=255)
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
