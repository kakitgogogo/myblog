from django.core.exceptions import ValidationError

class PasswordValidator:
    """
    Validate whether the password is of a minimum length.
    """
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                "This password is too short. It must contain at least {} character.".format(self.min_length),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return "Your password must contain at least {} character.".format(self.min_length)