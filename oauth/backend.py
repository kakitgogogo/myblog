import abc
import six
import logging
import requests
import json
from urllib import parse
from io import BytesIO
import uuid

from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files import File
from django.db import models

from .models import OAuthUser

logger = logging.getLogger(__name__)

@six.add_metaclass(abc.ABCMeta)
class BaseOAuthBackend(object):
    access_token = None
    platform = None

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_authorization_url(self, next_url):
        '''
        1. Users are redirected to third party authorization url
        '''

    @abc.abstractmethod
    def get_access_token(self, code):
        '''
        2. Redirects back to your site with a temporary code, 
           Exchange this code for an access token
        '''

    @abc.abstractmethod
    def get_user_info(self):
        '''
        3. Use the access token to access the API
        '''

    def request_get(self, url, params):
        response = requests.get(url=url, params=params)
        return response.text
    
    def request_post(self, url, data):
        response = requests.post(url=url, data=data)
        return response.text

class GithubOAuthBackend(BaseOAuthBackend):
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    API_URL = 'https://api.github.com/user'
    platform = 'github'

    def __init__(self):
        super().__init__()
        self.client_id = settings.OAUTH_SETTINGS['GITHUB']['CLIENT_ID']
        self.client_secret = settings.OAUTH_SETTINGS['GITHUB']['CLIENT_SECRET']
        self.callback_url = settings.OAUTH_SETTINGS['GITHUB']['CALLBACK_URL'] + '?platform=github'

    def get_authorization_url(self, next_url='/'):
        redirect_uri = self.callback_url + '&next=' + next_url
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': 'user',
        }
        url = self.AUTH_URL + '?' + parse.urlencode(params)
        return url
    
    def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        response = self.request_post(self.ACCESS_TOKEN_URL, params)
        try:
            msg = parse.parse_qs(response)
            self.access_token = msg['access_token'][0]
            return self.access_token
        except Exception as e:
            logger.error(e)
            return None

    def get_user_info(self):
        params = {
            'access_token': self.access_token
        }
        response = self.request_get(self.API_URL, params)
        try:
            info = json.loads(response) 
            userid = str(info['id'])
            nickname = info['login']
            email = info['email']
            avatar_url = info['avatar_url']
            platform = 'github'
            oauth_user = None
            try:
                oauth_user = OAuthUser.objects.get(userid=userid, platform=platform)
            except OAuthUser.DoesNotExist:
                imgfilename = str(uuid.uuid4().hex) + '.png'
                user = get_user_model().objects.create(
                    username=platform+'_'+userid, 
                    nickname=nickname, 
                    email=email,
                    mugshot=imgfilename
                )
                res = requests.get(avatar_url)
                image_bytes = BytesIO(res.content)
                user.mugshot.save(imgfilename, File(image_bytes))
                oauth_user = OAuthUser.objects.create(userid=userid, platform=platform, user=user)
                oauth_user.save()
            return oauth_user.user
        except Exception as e:
            logger.error(e)
            logger.info('Github response: ' + response)
            return None

def get_oauth_backend(platform):
    backends = BaseOAuthBackend.__subclasses__()
    backends = [x() for x in backends]
    result = list(filter(lambda x: x.platform == platform, backends))
    if result:
        return result[0]
    return None