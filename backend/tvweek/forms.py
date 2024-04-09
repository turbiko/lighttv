# chart/forms.py
from django import forms


class TVChartUploadForm(forms.Form):
    tv_chart_file = forms.FileField()

