from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
	qs = BlogPost.objects.published()[:5]
	context =  {'title': 'Welcome to Try Django', "blog_list" :qs}
	return render(request, "home.html", context)


def about_page(request):
	return render(request, 'about.html', {'title': 'About'})


def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form = ContactForm()
	context = {
		'title': 'Contact Us',
		'form' : form}
	return render(request, 'form.html', context)
