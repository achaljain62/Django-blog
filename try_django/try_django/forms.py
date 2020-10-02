from django import forms

class ContactForm(forms.Form):
	Name = forms.CharField()
	email = forms.EmailField()
	content = forms.CharField(widget = forms.Textarea)