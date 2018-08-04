from oauth.backend import get_oauth_backend
from django import template

register = template.Library()

@register.simple_tag
def get_authorization_url(platform, next_url):
    backend = get_oauth_backend(platform)
    if next_url.strip() == '':
        next_url = '/'
    return backend.get_authorization_url(next_url)