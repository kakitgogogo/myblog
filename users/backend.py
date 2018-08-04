from .models import BlogUser

class EmailOrUsernameBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = BlogUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except BlogUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return BlogUser.objects.get(pk=user_id)
        except BlogUser.DoesNotExist:
            return None