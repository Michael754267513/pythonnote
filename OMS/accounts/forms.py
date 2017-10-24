# --*-- coding:utf-8 --*--

from django import forms
from django.contrib.auth.models import Group, Permission
from models import User


class LoginUserForm(forms.Form):
    username = forms.CharField(
            label=u"登陆帐号",
            error_messages={'required': u'帐号不能为空'},
            widget=forms.TextInput(attrs={'placeholder': u"登陆帐号",}),
    )
    password = forms.CharField(
            label=u"密码",
            error_messages={'required': u'密码不能为空'},
            widget=forms.PasswordInput(attrs={'placeholder': u"密码",})
    )

    def clean_all(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginUserForm, self).clean()
        return cleaned_data


class UserForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=u"登陆帐号",
                                error_messages={'invalid': u"这个值仅可以包含字母,数字和@/./+/-/_字符."})
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=u"密码")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=u"密码(again)")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError("此用户名已经存在.")
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                    "这个邮箱地址已被使用. 请提供不同的邮箱地址."
            )
        return self.cleaned_data['email']

    def clean_password(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("两次输入密码不一致.")
        return self.cleaned_data


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'


class SetPasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原密码', error_messages={'required': u'请输入原密码'},
                                   widget=forms.PasswordInput(attrs={'placeholder': u'原密码',}),)
    new_password = forms.CharField(label=u'新密码', error_messages={'required': u'请输入新密码'},
                                   widget=forms.PasswordInput(attrs={'placeholder': u'新密码'}),)
    verify_password = forms.CharField(label=u'确认密码', error_messages={'required': u'请再一次输入新密码'},
                                      widget=forms.PasswordInput(attrs={'placeholder': u'确认密码',}),)

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'所有项都为必填')
        elif self.cleaned_data['new_password'] != self.cleaned_data['verify_password']:
            raise forms.ValidationError(u'输入密码不一致')
        else:
            cleaned_data = super(SetPasswordForm, self).clean()
        return cleaned_data

