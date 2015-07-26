from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import ObjectPaginator, InvalidPage
from djangogallery.tagging.models import TaggedItem
from djangogallery.middleware import threadlocals
from djangogallery.gallery.models import Photo
from django import newforms as forms
from django.newforms import ModelForm
from djangogallery.gallery.forms import PhotoForm, editPhotoForm, newPhotoForm, LoginForm, UserForm, changePasswordForm

## Index view
#
# Is the main view, displays the needed images eventually filtered by author or tag
# permits to logged users to upload new images
def index(request, template, user=None, tag=None, home=False):
    context = RequestContext(request)
    ## the logged user
    logged_as=threadlocals.get_current_user()
    photo_list = Photo.objects.all()
    title='Last uploaded'

    ## Uploading a new image
    if (request.POST):
        newform = newPhotoForm(request.POST,request.FILES)
        if newform.is_valid():
            newform.save()
            return HttpResponseRedirect('/yourphotos/')
    try:
        page=request.__getitem__('page')
    except KeyError:
        page=1

    ## Filtering by user
    if user:
        try:
            id=User.objects.get(username=user)
            photo_list = Photo.objects.filter(author=id)
            title=user+' pictures'
        except User.DoesNotExist:
            title='No photoes by '+user

    ## Filtering by tag
    if tag:
        photo_list = TaggedItem.objects.get_by_model(Photo, tag)
        title='Photoes tagged<br />"'+tag+'"'

    ## The user photoes
    if home:
        photo_list = Photo.objects.filter(author=logged_as)
        title='Your photoes'

    ## Pagination page number
    page_num=page;
    newform = newPhotoForm()
    return render_to_response(template, locals(), context_instance=context)


## edit view
#
# permits to a logged user to edit his own image infos
@login_required
def edit(request, template, id=None):
    context = RequestContext(request)

    if id:
        title='Edit the picture'
        try:
            oldphoto = Photo.objects.get(pk=id)
        except Photo.DoesNotExist:
            return HttpResponseRedirect('/yourphotos/')
        form = editPhotoForm(instance=oldphoto)

        if (request.POST):
            form = PhotoForm(request.POST,request.FILES,instance=oldphoto)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/yourphotos/')

    return render_to_response(template, locals(), context_instance=context)

## delete view
#
# permits to a logged user to delete his own image
@login_required
def delete(request, template, id=None):
    context = RequestContext(request)

    if id:
        Photo.objects.get(pk=id).delete()

    return HttpResponseRedirect('/yourphotos/')

## register view
#
#  User registration as in django-profile
def register(request, template):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            newuser = User.objects.create_user(username=username, email='', password=password)
            newuser.save()
            return HttpResponseRedirect('/login/')
    else:
        form = UserForm()
    return render_to_response(template, locals(), context_instance=context)

## login view
#
#  User login as in http://www.djangosnippets.org/snippets/332/
def login_view(request, template):
    context = RequestContext(request)

    #http://www.djangosnippets.org/snippets/332/
    if request.method == "POST":
        loginform = LoginForm(request.POST)
        if loginform.login(request):
            return HttpResponseRedirect('/')
    else:
        loginform = LoginForm()

    return render_to_response(template, locals(), context_instance=context)

## logout view
#
#  User logout
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')

## change password view
#
#  Change the password of the authenticated user as in django-profile
@login_required
def change_password(request, template):

    context = RequestContext(request)
    if request.method == "POST":
        form = changePasswordForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/')
    else:
        form = changePasswordForm()

    return render_to_response(template, locals(), context_instance=context)