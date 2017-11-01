from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from auth.auth import log_required
from client.gets import get_sales_posts, get_social_p, get_social_posts
from client.puts import update_post_image, update_post_text, update_comment, update_sale, update_sale_image
from client.posts import new_comment, new_post, new_post_image, new_sale, new_sale_image
from client.deletes import delete_comment, delete_post
from posts.forms import *
from django.http import HttpResponseRedirect
import os
import time


class IndexView(TemplateView):

    template_name = 'posts/posts_index.html'

    @log_required
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class SocialView(TemplateView):

    template_name = 'posts/posts_social.html'

    @log_required
    def get(self, request, *args, **kwargs):
        posts_list = []
        form = EditPostForm()
        for post in get_social_posts()[1]:
            imagen_default = "Sin imagen"
            if 'image' in post:
                imagen_default = post['image']
            posts_list.append({
                'post': post['_id'],
                'autor': post['author']['_id'],
                'autor_nick': post['author']['nickname'],
                'imagen': imagen_default,
                'cuerpo': post['text'],
            })
        return render(request, self.template_name, {'posts': posts_list, 'form': form, })

    @log_required
    def post(self, request, *args, **kwargs):
        form = EditPostForm(request.POST, request.FILES)
        if form.is_valid():
            update_post_text(form.cleaned_data['id'], form.cleaned_data['text'])
            if len(request.FILES) > 0:
                _, extension = os.path.splitext(request.FILES['photo'].name)
                path_file = 'media/' + str(int(time.time())) + extension
                with open(path_file, 'wb+') as destination:
                    for chunk in request.FILES['photo'].chunks():
                        destination.write(chunk)
                    update_post_image(form.cleaned_data['id'], path_file)
        return redirect("posts:social")


class SalesView(TemplateView):

    template_name = 'posts/posts_sales.html'

    @log_required
    def get(self, request, *args, **kwargs):
        sales_list = []
        form = EditSaleForm()
        for sale in get_sales_posts()[1]:
            imagen_default = "Sin imagen"
            if 'image' in sale:
                imagen_default = sale['image']
            sales_list.append({
                'sale': sale['_id'],
                'author': sale['author']['_id'],
                'nick': sale['author']['nickname'],
                'price': sale['price'],
                'imagen': imagen_default,
                'cuerpo': sale['text'],
                'tags': ",".join(sale['tags']),
            })
        return render(request, self.template_name, {'sales': sales_list, 'form': form, })

    @log_required
    def post(self, request, *args, **kwargs):
        form = EditSaleForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) > 0:
                _, extension = os.path.splitext(request.FILES['image'].name)
                path_file = 'media/' + str(int(time.time())) + extension
                with open(path_file, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                    update_sale_image(form.cleaned_data['id'],
                                      form.cleaned_data['price'],
                                      path_file,
                                      form.cleaned_data['text'],
                                      form.cleaned_data['tags'])
            else:
                update_sale(form.cleaned_data['id'],
                            form.cleaned_data['price'],
                            form.cleaned_data['text'],
                            form.cleaned_data['tags'])
        return redirect("posts:sales")



class CommentsView(TemplateView):

    template_name = 'posts/posts_comments.html'

    @log_required
    def get(self, request, *args, **kwargs):
        post_search = request.GET.get("post_search")
        if post_search is not None:
            form = EditCommentForm()
            _, post = get_social_p(post_search)
            comments_list = []
            if "comments" in post:
                for comment in post['comments']:
                    comments_list.append({
                        'id': comment["_id"],
                        'autor': comment['author']['_id'],
                        'autor_name': comment['author']['nickname'],
                        'text': comment['text'],
                    })
            return render(request, self.template_name, {'post_id': post_search, 'comments': comments_list, 'form': form, })

        return redirect("posts:social")

    @log_required
    def post(self, request, *args, **kwargs):
        form = EditCommentForm(request.POST)
        if form.is_valid():
            print(request.POST.get("post_id"), form.cleaned_data['id'], form.cleaned_data['text'])
            update_comment(request.POST.get("post_id"), form.cleaned_data['id'], form.cleaned_data['text'])
            next_page = request.POST.get('next', '/')
            return HttpResponseRedirect(next_page)
        return redirect("posts:social")


class NewCommentsView(TemplateView):

    template_name = 'posts/posts_new_comment.html'

    @log_required
    def get(self, request, *args, **kwargs):
        post_search = request.GET.get("post_search")
        back = request.GET.get("back")
        if post_search is not None:
            form = NewCommentForm()
            return render(request, self.template_name, {'form': form, 'post_id': post_search, 'back': back, })

        return redirect("posts:social")

    @log_required
    def post(self, request, *args, **kwargs):
        form = NewCommentForm(request.POST)
        back = request.POST.get('back', '/')
        if form.is_valid():
            new_comment(request.POST.get('id'), form.cleaned_data['author'], form.cleaned_data['text'])
            return HttpResponseRedirect(back)
        else:
            return render(request, self.template_name, {'form': form, 'post_id': request.POST.get('id'), 'back': back, })
        return redirect("posts:social")


@log_required
def remove_comment(request):
    if request.method == "POST":
        delete_comment(request.POST.get("post_id"), request.POST.get("comment_id"))
        next_page = request.POST.get('next', '/')
        return HttpResponseRedirect(next_page)
    return redirect("posts:social")


@log_required
def remove_post(request):
    if request.method == "POST":
        delete_post(request.POST.get("post_id"))
    return redirect("posts:social")


@log_required
def remove_sale(request):
    if request.method == "POST":
        delete_post(request.POST.get("post_id"))
    return redirect("posts:sales")


class NewSocialView(TemplateView):

    template_name = 'posts/posts_new_social.html'

    @log_required
    def get(self, request, *args, **kwargs):
        form = NewPostForm()
        return render(request, self.template_name, {'form': form, })

    @log_required
    def post(self, request, *args, **kwargs):
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) > 0:
                _, extension = os.path.splitext(request.FILES['image'].name)
                path_file = 'media/' + str(int(time.time())) + extension
                with open(path_file, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                    new_post_image(form.cleaned_data['author'], path_file, form.cleaned_data['text'])
            else:
                new_post(form.cleaned_data['author'], form.cleaned_data['text'])
            return redirect("posts:social")
        return render(request, self.template_name, {'form': form, })


class NewSalesView(TemplateView):

    template_name = 'posts/posts_new_sales.html'

    @log_required
    def get(self, request, *args, **kwargs):
        form = NewSaleForm()
        return render(request, self.template_name, {'form': form, })

    @log_required
    def post(self, request, *args, **kwargs):
        form = NewSaleForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) > 0:
                _, extension = os.path.splitext(request.FILES['image'].name)
                path_file = 'media/' + str(int(time.time())) + extension
                with open(path_file, 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
                    new_sale_image(form.cleaned_data['author'],
                                   form.cleaned_data['price'],
                                   path_file,
                                   form.cleaned_data['text'],
                                   form.cleaned_data['tags'])
            else:
                new_sale(form.cleaned_data['author'],
                         form.cleaned_data['price'],
                         form.cleaned_data['text'],
                         form.cleaned_data['tags'])
            return redirect("posts:sales")
        return render(request, self.template_name, {'form': form, })
