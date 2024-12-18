from django.shortcuts import render
import datetime
from django.conf import settings
from .models import Category

def index(request):
    categories = []
    if request.user.is_authenticated:
        categories = Category.objects.filter(author__pk = request.user.pk).all()
    else:
        incognito_token = request.COOKIES.filter('incognito_token')
        if incognito_token:
            categories = Category.objects.filter(incognito_user_token = incognito_token).all()
            
    return render(request, 'categories/index.html', {'categories': categories})


# funkcja pomocnicza dla ustalenia cookie (głównie jest wykorzystywana dla trybu incognito)
def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )