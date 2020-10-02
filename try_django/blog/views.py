from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost
from .forms import BlogCreatePost

# Create your views here.

#CRUD

def blog_post_list_view(request):
	qs = BlogPost.objects.published()
	if request.user.is_authenticated:
		my_qs = BlogPost.objects.filter(user=request.user)
		qs = (qs | my_qs).distinct()
	template_name = "blog/list.html"
	context = {"objects_list": qs}
	return render(request, template_name, context )

# @login_required()
@staff_member_required
def blog_post_create_view(request):
	
	form = BlogCreatePost(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.save()
		obj.user = request.user()
		form = BlogCreatePost()
	
	template_name = "form.html"
	context = {"form": form, 'title': 'Create New Post'}
	return render(request, template_name, context )

def blog_post_detail_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	template_name = "blog/detail.html"
	context = {"object": obj}
	return render(request, template_name, context )


@staff_member_required
def blog_post_update_view(request,slug):

	obj = get_object_or_404(BlogPost,slug=slug)

	form = BlogCreatePost(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()

	template_name = "form.html"
	context = {"form": form, 'title': f'Update - {obj.title}'}
	return render(request, template_name, context )

@staff_member_required
def blog_post_delete_view(request, slug):
	obj = get_object_or_404(BlogPost, slug=slug)
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	template_name = "blog/delete.html"
	context = {"object": obj}
	return render(request, template_name, context )



