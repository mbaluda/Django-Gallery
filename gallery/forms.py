from django import newforms as forms
from django.core.exceptions import ObjectDoesNotExist
from djangogallery.gallery.models import Photo
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
import magic

##  Login Form
#
#http://www.djangosnippets.org/snippets/332/
class LoginForm(forms.Form):
        username = forms.CharField(label=_('username'))
        password = forms.CharField(label=_('password'), widget = forms.PasswordInput)
        user = None   # allow access to user object
        def clean(self):
            ## only do further checks if the rest was valid
            if self._errors: return

            from django.contrib.auth import login, authenticate
            user = authenticate(username=self.data['username'],
                                password=self.data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user
                else:
                    raise forms.ValidationError(ugettext(
                        'This account is currently inactive. Please contact '
                        'the administrator if you believe this to be in error.'))
            else:
                raise forms.ValidationError(ugettext(
                    'The username and password you specified are not valid.'))
        def login(self, request):
            from django.contrib.auth import login
            if self.is_valid():
                login(request, self.user)
                return True
            return False

##  PhotoForm
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('author','posted')

##  newPhotoForm
class newPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('caption','author','posted','tag')

##  editPhotoForm
class editPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('image','author','posted')

## User form
#
#http://code.google.com/p/django-profile/
class UserForm(forms.Form):
    username = forms.CharField(max_length=255, min_length = 3)
    password1 = forms.CharField(min_length=6, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=6, widget=forms.PasswordInput)

    def clean_username(self):
        """
        Verify that the username isn't already registered
        """
        username = self.cleaned_data.get("username")
        if not set(username).issubset("abcdefghijklmnopqrstuvwxyz0123456789_-"):
            raise forms.ValidationError(_("That username has invalid characters."))

        if len(User.objects.filter(username=username)) == 0:
            return username
        else:
            raise forms.ValidationError(_("The username is already registered."))

    def clean(self):
        """
        Verify that the 2 passwords fields are equal
        """
        if self.cleaned_data.get("password1") == self.cleaned_data.get("password2"):
            return self.cleaned_data
        else:
            raise forms.ValidationError(_("The passwords inserted are different."))

## User form
#
#http://code.google.com/p/django-profile/
class changePasswordForm(forms.Form):
    newpass1 = forms.CharField( min_length = 6, widget = forms.PasswordInput )
    newpass2 = forms.CharField( min_length = 6, widget = forms.PasswordInput )

    def clean(self):
        """
        Verify the equality of the two passwords
        """

        if self.cleaned_data.get("newpass1") and self.cleaned_data.get("newpass1") == self.cleaned_data.get("newpass2"):
            return self.cleaned_data
        else:
            raise forms.ValidationError(_("The passwords inserted are different."))

    def save(self, user):
        "Saves the new password."
        user.set_password(self.cleaned_data.get('newpass1'))
        user.save()