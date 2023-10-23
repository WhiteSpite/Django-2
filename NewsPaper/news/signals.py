from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Post


@receiver(m2m_changed, sender=Post.categories.through)
def mailing_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        post = instance
        users_for_mailing = set()
        categories = ''
        for category in post.categories.all():
            categories += f'{category.name}, '
            for subscriber in category.subscribers.all():
                if subscriber.email:
                    users_for_mailing.add(subscriber)
        if users_for_mailing:
            categories = categories[:-2]
            for user in users_for_mailing:
                msg = EmailMultiAlternatives(
                    subject=f'New Post! ({categories}) by {post.author.user.username}',
                    body=f'{post.title.upper()}\n\n{post.content}',
                    from_email='iliab02@yandex.ru',
                    to=[user.email],
                )
                msg.send()
