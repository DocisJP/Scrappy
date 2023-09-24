from django import forms

class ScrapeHistoryDataForm(forms.Form):
    year_or_title = forms.CharField(label='Title', max_length=100, help_text="Enter a year a title to scrape data.")
