import requests
from django.shortcuts import render, redirect

from core.settings import API_URL as root
from utils.decorators import user_login_required

root += 'auth'


def login(request):
    if 'user_id' in request.COOKIES:
        return redirect('/reviews/')
    if request.method == 'GET':
        return render(request, 'login_form.html')

    user_id = request.POST['user_id']
    pwd = request.POST['pwd']
    data = {
        'id': user_id,
        'pwd': pwd
    }
    r = requests.post(
        f'{root}/login/',
        headers={'X-CSRFTOKEN': request.COOKIES.get('csrftoken')},
        data=data
    )
    # print(r.cookies.get_dict())
    result = r.json()
    if result['success'] is True:
        ret = redirect('/reviews/')
        ret.set_cookie('sessionid', result['sessionid'])
        ret.set_cookie('user_id', user_id)
        return ret
    else:
        return redirect('/login/')


@user_login_required
def logout(request):
    r = requests.post(
        f'{root}/logout/',
        headers={'X-CSRFTOKEN': request.COOKIES.get('csrftoken')},
        cookies={'sessionid': request.COOKIES['sessionid']}
    )
    ret = redirect('/login/')
    ret.delete_cookie('user_id')
    ret.delete_cookie('sessionid')
    return ret

