from datetime import datetime

from django.contrib.auth import views as auth_views
from django.core.exceptions import (ObjectDoesNotExist, PermissionDenied,
                                    ValidationError)
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.loader import get_template
from django.utils.timezone import make_aware

from core.models import MyUser, Token
from core.services import TokenService

from .forms import PasswordResetForm

def handler404(request, exception, template_name='app/error.html'):
    return render(request, template_name, {'message': 'Not found', 'submessage': exception})

def confirmAccount(request, chef_uuid, token):
    user = MyUser.objects.get(uuid=chef_uuid)
    try:
        tokenService = TokenService.get_from(token)

        tokenService.is_type(Token.TYPE_USER_CONFIRM, raise_exception=True)
        tokenService.check_expired( raise_exception=True)
    except ObjectDoesNotExist:
        tokenService.delete()
        raise Http404('Invalid token. This account may be confirmed already.')
    except ValidationError:
        tokenService.delete()
        raise Http404('Token has expired')

    user.is_confirmed = True
    user.save()
    tokenService.delete(raise_exception=True)

    return render(request, 'app/confirm_successful.html', {'username': user.username})

def passwordReset(request, chef_uuid, token):
    user = MyUser.objects.get(uuid=chef_uuid)
    tokenService = TokenService.get_from(token)

    tokenService.is_type(Token.TYPE_PASSWORD_RESET, raise_exception=True)
    tokenService.check_expired(raise_exception=True)

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            tokenService.delete()

    else:
        form = PasswordResetForm()
    

    return render(request, 'app/password_reset.html', {
                'form': form
            })
