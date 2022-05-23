import requests
from django.shortcuts import render, redirect

from core.settings import API_URL as root
from utils.decorators import user_login_required
from views.auth_views import logout

root += 'book_review'


@user_login_required
def index(request):
    r = requests.get(f'{root}/all/', cookies={'sessionid': request.COOKIES['sessionid']})
    if r.status_code == 401:
        return redirect('/logout/')

    result = r.json()
    books = result['data']
    return render(request, 'index.html', {'books': books})


@user_login_required
def detail(request, pk):
    r = requests.get(f'{root}/get/{pk}/', cookies={'sessionid': request.COOKIES['sessionid']})
    result = r.json()
    if result['success'] is True:
        book = result['data']
        return render(request, 'detail.html', {'book': book})
    else:
        message = result['message']
        return render(request, 'result.html', {'message': message})


@user_login_required
def search(request):
    user_id = request.GET.get('user_id')
    r = requests.get(
        f'{root}/get_critic_reviews/',
        params={'user_id': user_id},
        cookies={'sessionid': request.COOKIES['sessionid']}
    )
    data = r.json()
    books = data['data']
    return render(request, 'critic_reviews.html', {'books': books})


@user_login_required
def add(request):
    if request.method == 'GET':
        return render(request, 'add_form.html')

    title = request.POST['title']
    name = request.POST['name']
    comment = request.POST['comment']
    data = {
        'user_id': request.COOKIES['user_id'],
        'title': title,
        'name': name,
        'comment': comment
    }
    r = requests.post(
        f'{root}/add/',
        data=data,
        cookies={'sessionid': request.COOKIES['sessionid']}
    )
    result = r.json()
    return render(request, 'result.html', {'message': result['message']})


@user_login_required
def edit(request):
    if request.method == 'GET':
        return render(request, 'edit_form.html')

    book_no = request.POST['book_no']
    title = request.POST['title']
    name = request.POST['name']
    comment = request.POST['comment']

    data = {
        'user_id': request.COOKIES['user_id'],
        'title': title,
        'name': name,
        'comment': comment
    }

    r = requests.post(
        f'{root}/edit/{book_no}/',
        data=data,
        cookies={'sessionid': request.COOKIES['sessionid']}
    )
    result = r.json()
    return render(request, 'result.html', {'message': result['message']})


@user_login_required
def delete(request):
    if request.method == 'GET':
        return render(request, 'delete_form.html')

    book_no = request.POST['book_no']
    data = {
        'user_id': request.COOKIES['user_id']
    }
    r = requests.post(
        f'{root}/delete/{book_no}/',
        data=data,
        cookies={'sessionid': request.COOKIES['sessionid']}
    )

    result = r.json()
    return render(request, 'result.html', {'message': result['message']})
