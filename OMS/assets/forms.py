# --*-- coding:utf8 --*--

from django import forms
from models import Assets, Hardware, Network, Services, Tag


class HardwareForm(forms.ModelForm):

    class Meta:
        model = Hardware
        fields = '__all__'


class AssetsForm(forms.ModelForm):
    networks = forms.ModelChoiceField(queryset=Network.objects.filter(bind=0))

    class Meta:
        model = Assets
        fields = '__all__'


class AssetsEditForm(forms.ModelForm):

    class Meta:
        model = Assets
        fields = '__all__'


class NetworkForm(forms.ModelForm):

    class Meta:
        model = Network
        fields = '__all__'


class ServicesForm(forms.ModelForm):

    class Meta:
        model = Services
        fields = '__all__'


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'
