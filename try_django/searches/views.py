from django.shortcuts import render
from .models import Searching
from blog.models import BlogPost

# Create your views here.

def search_view(request):
	query = request.GET.get("q", None)
	user = None
	tempate_name = "searches/search.html"
	context = { 'query': query}

	if request.user.is_authenticated:
		user = request.user
	if query is not None:
		Searching.objects.create(user=user, query=query)
		blog_list = BlogPost.objects.search(query)
		context["blog_list"] = blog_list

	return render(request, tempate_name, context)