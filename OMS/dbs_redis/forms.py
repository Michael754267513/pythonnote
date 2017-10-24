# --*-- coding:utf8 --*--

from django import forms
from models import Redis


class RedisForm(forms.ModelForm):

    class Meta:
        model = Redis
        fields = '__all__'
