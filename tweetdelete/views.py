# -*- encoding: utf-8 -*-
from django.shortcuts import render
import tweetpony
from tweetdelete.forms import AuthForm
from tweetdelete.models import Data
from django.core.context_processors import csrf

CONSUMER_KEY = 'qoHxj86rXhfEbDsT00DflA'
CONSUMER_SECRET = 'PxRKaEkSlI3Il5jX7uUgAuOPR7WtGnMa8uw5WeI'

def get_api(request):
    try:
        access_data = Data.objects.all()[0]
        api = tweetpony.API(CONSUMER_KEY, CONSUMER_SECRET, access_data.access_token, access_data.access_token_secret)
    except tweetpony.APIError as err:
        data = {
            'errors' : [{'code': err.code, 'description' : err.description},],
        }
        return data
        #return render(request, 'auth.html',{ 'data' : data })
    except:
        return authenticate(request)
    else:
        data = {
            'api': api,
        }
        return data
    return False


def authenticate(request, api=None):
    try:
        api = tweetpony.API(CONSUMER_KEY, CONSUMER_SECRET)
    except tweetpony.APIError as err:
        data = {
            'errors' : [{'code': err.code, 'description' : err.description},],
        }
        return data
        #return render(request, 'auth.html',{ 'data' : data })

    if request.POST:
        form = AuthForm(request.POST)
        if form.is_valid():
            # Falla porque es OTRO objeto api al llegar acá
            verifier = form.cleaned_data['verifier']
            try:
                api.authenticate(verifier)
            except tweetpony.APIError as err:
                data = {
                    'errors' : [{'code': err.code, 'description' : err.description},],
                }
                return data
                #return render(request, 'auth.html',{ 'data' : data, })
            else:
                access_data = Data(
                    access_token = api.access_token,
                    access_token_secret = api.access_token_secret,
                )
                access_data.save()
                data = {
                    'api' : api,
                }
                return data

    url = api.get_auth_url()
    form = AuthForm()
    data = {
        'url' : url,
        'form' : form,
    }
    return data
    #return render(request, 'auth.html', {'data' : data })


def principal(request):

    data = get_api(request)
    if 'api' in data.keys():
        api = data['api']
    else:
        return render(request, 'auth.html', {'data' : data })

    user = api.user
    #api.update_status(status = 'Testing')
    a = 1
    tweets_per_page = 3
    timeline = api.user_timeline(count=tweets_per_page)
    while True:
        for tweet in timeline:
            print tweet.text
            id = tweet.id
        a+=1
        if len(timeline) != tweets_per_page or a==5:
            break
        timeline += api.user_timeline(count=tweets_per_page, max_id=id-1)

    data = {
        'timeline': timeline,
    }

    return render(request, 'inicio.html',{ 'data' : data })

