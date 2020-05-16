from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.timezone import make_aware

from core.models import Token


class EmailService:
    def send_mail(self, template: str, subject: str,  recipients: [str], data: dict = None):
        html_body = get_template(
            'api/emails/{}'.format(template)
        ).render(data)

        send_mail(
            subject,
            html_body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            html_message=html_body
        )


class TokenService:
    @classmethod
    def get_from(cls, token_ref: str):
        return TokenService(Token.objects.get(token=token_ref))

    @classmethod
    def create(cls, reference: str, type: str, delta: int):
        return TokenService(
            Token.objects.create(
                reference=reference,
                type=type,
                valid_until=make_aware(datetime.now()) + delta
            )
        )

    def __init__(self, token: Token = None):
        self.token = token

    def _check_has_token(self, raise_exception=False):
        has_token = self.token is not None

        if not has_token and raise_exception:
            raise ObjectDoesNotExist('No token passed to TokenService')

        return has_token

    def get_token(self):
        return self.token

    def check_expired(self, raise_exception = False):
        self._check_has_token()

        expired = make_aware(datetime.now()) > self.token.valid_until
        if expired:
            self.token.delete()
            if raise_exception:
                raise ValidationError(message="Token has expired")

        return expired

    def is_type(self, type, raise_exception=False):
        valid = self.token.type == type

        if raise_exception and not valid:
            raise ObjectDoesNotExist

        return valid

    def delete(self, raise_exception=False):
        if self._check_has_token(raise_exception=raise_exception):
            self.token.delete()

        self.token = None
