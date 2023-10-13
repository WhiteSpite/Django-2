from news.models import *

user1 = User.objects.create_user(username='John', email='email1@mail.ru', password='11111111')
user2 = User.objects.create_user(username='Ivan', email='email2@mail.ru', password='22222222')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Political')
category3 = Category.objects.create(name='War')
category4 = Category.objects.create(name='Science')

post1 = Post.objects.create(author=author1, post_type='article', title='Title 1', content='Content 1')
post2 = Post.objects.create(author=author2, post_type='article', title='Title 2', content='Content 2')
news1 = Post.objects.create(author=author1, post_type='news', title='Title 3', content='Content 3')

post1.categories.add(category1, category2, category3)
post2.categories.add(category4)
news1.categories.add(category2, category4)

comment1 = Comment.objects.create(post=post1, user=user1, text='Thanks for your work. Very interesting')
comment2 = Comment.objects.create(post=post1, user=user2, text='Good article! Go on')
comment3 = Comment.objects.create(post=post2, user=user1, text='Delusion')
comment4 = Comment.objects.create(post=news1, user=user1, text='It is Republican propaganda.')

comment4.like()
comment4.like()
comment4.like()
comment4.dislike()
comment3.like()
comment3.like()
comment2.dislike()
comment2.dislike()
comment2.dislike()
comment1.like()
comment1.like()
comment1.like()
comment1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.like()
post1.dislike()
post2.like()
news1.dislike()
news1.dislike()
news1.dislike()
news1.dislike()
news1.dislike()
news1.dislike()
news1.dislike()

author1.update_rating()
author2.update_rating()

Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]

best_post = Post.objects.all().order_by('-rating')[:1]
best_post.values('created_at', 'author__user__username', 'rating', 'title')[0]
best_post[0].preview()

Comment.objects.filter(post=best_post).values('created_at', 'user__username', 'rating', 'text')
