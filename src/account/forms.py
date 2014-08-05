from __future__ import absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        render_value = kwargs.pop('render_value', False)
        kwargs['widget'] = forms.PasswordInput(render_value=render_value,
                                               attrs={'placeholder':
                                                          _('Password')})
        super(PasswordField, self).__init__(*args, **kwargs)


class SetPasswordField(PasswordField):
    def clean(self, value):
        value = super(SetPasswordField, self).clean(value)
        min_length = 6
        if len(value) < min_length:
            raise forms.ValidationError(_("Password must be a minimum of {0} "
                                          "characters.").format(min_length))
        return value


class UserForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(UserForm):
    oldpassword = PasswordField(label=_("Current Password"))
    password1 = SetPasswordField(label=_("New Password"))
    password2 = PasswordField(label=_("New Password (again)"))

    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_("Please type your current"
                                          " password."))
        return self.cleaned_data["oldpassword"]

    def clean_password2(self):
        if ("password1" in self.cleaned_data
            and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data["password2"]

    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()


class SetPasswordForm(UserForm):
    password1 = SetPasswordField(label=_("Password"))
    password2 = PasswordField(label=_("Password (again)"))

    def clean_password2(self):
        if ("password1" in self.cleaned_data
            and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same password"
                                              " each time."))
        return self.cleaned_data["password2"]

    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()


class ResetPasswordKeyForm(forms.Form):
    password1 = SetPasswordField(label=_("New Password"))
    password2 = PasswordField(label=_("New Password (again)"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.temp_key = kwargs.pop("temp_key", None)
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)

    # FIXME: Inspecting other fields -> should be put in def clean(self) ?
    def clean_password2(self):
        if ("password1" in self.cleaned_data
            and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"]
                    != self.cleaned_data["password2"]):
                raise forms.ValidationError(_("You must type the same"
                                              " password each time."))
        return self.cleaned_data["password2"]

    def save(self):
        # set the new user password
        user = self.user
        user.set_password(self.cleaned_data["password1"])
        user.save()
