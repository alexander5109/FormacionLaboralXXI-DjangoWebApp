from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.views import View, generic
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
# from aplicacion import models, forms as aplicacion_models, aplicacion_forms
from functools import wraps
import random
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404

# Create your views here.



class PostList(generic.ListView):
	queryset = models.Post.objects.filter(status=1).order_by('-created_on')
	template_name = 'blog/index.html'

class PostDetail(generic.DetailView):
	model = models.Post
	template_name = 'blog/post_detail.html'
	
def post_detail(request, slug):
	template_name = 'blog/post_detail.html'
	post = get_object_or_404(models.Post, slug=slug)
	comments = post.comments.filter(active=True)
	new_comment = None    # Comment posted
	if request.method == 'POST':
		comment_form = forms.CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()
	else:
		comment_form = forms.CommentForm()
	return render(request, template_name, {'post': post,
										   'comments': comments,
										   'new_comment': new_comment,
										   'comment_form': comment_form})