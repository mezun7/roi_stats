from django import forms

from roi.models import Olympiad


class RegionCsvImportForm(forms.Form):
    csv_file = forms.FileField()


class OlympiadResultCsvImportForm(forms.Form):
    olympiad = forms.ModelChoiceField(queryset=Olympiad.objects.all().order_by('date_from'))
    csv_file = forms.FileField()
