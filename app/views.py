from datetime import datetime

from django.contrib.auth import views as auth_views
from django.core.exceptions import (ObjectDoesNotExist, PermissionDenied,
                                    ValidationError)
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.loader import get_template
from django.utils.timezone import make_aware

from core.models import MyUser, Token


def confirmAccount(request, chef_uuid, token):
    user = MyUser.objects.get(uuid=chef_uuid)
    token = Token.objects.get(token=token)

    if not token or not user or token.type != Token.TYPE_USER_CONFIRM:
        raise ObjectDoesNotExist

    if make_aware(datetime.now()) > token.valid_until:
        token.delete()
        raise ValidationError(message="Token has expired")

    user.is_confirmed = True
    user.save()
    token.delete()

    return HttpResponse(
        get_template('app/confirm_successful.html').render({"username": user.username})
    )
