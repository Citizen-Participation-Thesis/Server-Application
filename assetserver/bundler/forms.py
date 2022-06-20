from django import forms
from django.forms import TextInput
from .models import MaterialPrefix, ModelFile, Material, SwappableGroup, Project


class CreateSwappableGroupForm(forms.Form):
    name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name'}))

    def clean(self):
        cleaned_data = self.cleaned_data

        try:
            SwappableGroup.objects.get(name=cleaned_data['name'], connected=False)
        except SwappableGroup.DoesNotExist:
            pass
        else:
            self.add_error('name', 'Group already exists')

        return cleaned_data


class CreateMaterialForm(forms.Form):
    hex_color = forms.CharField(widget=TextInput(attrs={'type': 'color'}), required=True)


# Need this to overwrite styling (aka get custom colors)
class MySelect(forms.SelectMultiple):
    option_template_name = 'widgets/coloredOptions.html'


class CreatePrefixesForm(forms.Form):
    prefix = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Prefix'}))
    materials = forms.ModelMultipleChoiceField(
        queryset=Material.objects.filter(connected=False),
        required=True,
        help_text='Select materials',
        widget=MySelect(),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        self.fields['materials'].validators = []
        try:
            MaterialPrefix.objects.get(prefix=cleaned_data['prefix'], connected=False)
        except MaterialPrefix.DoesNotExist:
            pass
        else:
            self.add_error('name', 'Prefix already exists')

        return cleaned_data


class CreateModelFileForm(forms.Form):
    presentable_name = forms.CharField(max_length=40, required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    model_base = forms.FileField(required=True)
    placeable = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'boolCheck'}), required=False)

    prefixes = forms.ModelMultipleChoiceField(
        queryset=MaterialPrefix.objects.filter(connected=False),
        required=False,
        help_text='Material prefixes (optional)'
    )

    group = forms.ModelChoiceField(
        queryset=SwappableGroup.objects.all(),
        required=False,
        help_text='Group (optional)'
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            ModelFile.objects.get(hidden_name=''.join(cleaned_data['presentable_name'].split()).lower())
        except ModelFile.DoesNotExist:
            pass
        else:
            self.add_error('presentable_name', 'Name too similar to: '+ModelFile.objects.get(
                hidden_name=''.join(cleaned_data['presentable_name'].split()).lower()).presentable_name)

        return cleaned_data


class CreateProjectForm(forms.Form):
    title = forms.CharField(max_length=40, min_length=1, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Title'}))
    description = forms.CharField(max_length=400, min_length=1, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Description'}))

    model_files = forms.ModelMultipleChoiceField(
        queryset=ModelFile.objects.all().order_by('presentable_name'),
        required=True,
        help_text='Select associated 3D models'
    )


class CreateDeployForm(forms.Form):
    selected_project = forms.ModelChoiceField(
        queryset=Project.objects.all().filter(status='Not deployed'),
        required=True,
        help_text='Select project to deploy'
    )


class CreatePauseForm(forms.Form):
    selected_project = forms.ModelChoiceField(
        queryset=Project.objects.all().filter(status='Deployed'),
        required=True,
        help_text='Select project to deploy',
    )

