# --*-- coding:utf8 --*--

from django import forms
from models import Databases


# class DBAForm(forms.ModelForm):
#     class Meta:
#         model = DBAccounts
#         fields = '__all__'


class DatabasesForm(forms.ModelForm):

    class Meta:
        model = Databases
        fields = '__all__'
