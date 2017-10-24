# --*-- coding:utf8 --*--

from django import forms
from models import Zone, Information, Upload, Path, Produce, Domain
from repository.models import Repository


class ZoneForm(forms.ModelForm):

    class Meta:
        model = Zone
        fields = '__all__'


class ZoneEditForm(forms.ModelForm):

    class Meta:
        model = Zone
        fields = '__all__'


class InformationForm(forms.ModelForm):

    class Meta:
        model = Information
        fields = '__all__'


class UploadForm(forms.ModelForm):

    class Meta:
        model = Upload
        fields = '__all__'


class PathForm(forms.ModelForm):

    class Meta:
        model = Path
        fields = '__all__'


class ProduceForm(forms.ModelForm):
    zones = forms.ModelMultipleChoiceField(label=u'选择分区', widget=forms.CheckboxSelectMultiple(),
                                           queryset=Zone.objects.all())
    config_file = forms.ModelChoiceField(label=u'模板文件', queryset=Upload.objects.all())
    generate_path = forms.ModelChoiceField(label=u'生成文件', queryset=Path.objects.filter(path_key__contains=u'配置生成目录'))
    project_name = forms.ModelChoiceField(label=u'对应仓库项目', queryset=Repository.objects.all())

    class Meta:
        model = Produce
        fields = '__all__'


class DomainForm(forms.ModelForm):

    class Meta:
        model = Domain
        fields = '__all__'
