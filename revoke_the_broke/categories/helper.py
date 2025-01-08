import datetime
from django.conf import settings
from .models import Category
from django.http import HttpRequest, HttpResponse

# helper function for setting cookies (mainly used for incognito mode)
def set_cookie(response: HttpResponse, key, value, days_expire=365):
    max_age = days_expire * 24 * 60 * 60
    
    expires = datetime.datetime.strftime(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    
    #set cookie to response that will be returned to user
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )
    
    
'''
    function to get one or all categories attached to user
'''
def get_categories(request: HttpRequest, id: int = -1):
    if request.user.is_authenticated:
        if id == -1:
            return Category.objects.filter(author__pk = request.user.pk).all() # search by authentiacted user id 
        else:
            return Category.objects.filter(author__pk = request.user.pk, pk=id).first()
    else:
        incognito_token = request.COOKIES.get('incognito_token')
        if incognito_token:
            if id == -1:
                return Category.objects.filter(incognito_user_token = incognito_token).all()
            else:
                return Category.objects.filter(incognito_user_token = incognito_token, pk=id).first()
        
    return []