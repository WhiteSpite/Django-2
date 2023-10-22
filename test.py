from timer import timer
import re

uri = 'http://127.0.0.1:8000/news/2/edit/'


def c(uri):
    uri = re.sub('\w+/\Z', '', uri)


def a(uri):
    uri = uri[::-1].split('/', 1)[-1][::-1]


def b(uri):
    for i in uri[:-1][::-1]:
        if i != '/':
            uri = uri[:-1]
        else:
            break
        
def v(uri):
    for k, i in enumerate(uri[:-1][::-1]):
        if i == '/':
            uri = uri[:-k]
            break


with timer():
    uri = 'http://127.0.0.1:8000/news/2/edit/'
    for i in range(2000000):
        a(uri)
