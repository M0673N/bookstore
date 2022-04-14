from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from bookstore.news.forms import ArticleForm, ArticleCommentForm
from .models import ArticleComment

from .signals import *
from django.db.models import signals


class ListArticlesView(ListView):
    template_name = 'articles/news.html'
    context_object_name = 'articles'
    model = Article
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.order_by('-date_posted')
        return context


class AddArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('news')
    template_name = 'articles/add_article.html'

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            signals.pre_save.disconnect(receiver=delete_old_image_on_article_change, sender=Article)
            article = form.save(commit=False)
            article.user = self.request.user
            article.save()
            signals.pre_save.connect(receiver=delete_old_image_on_article_change, sender=Article)
            return redirect('news')
        else:
            return render(request, 'articles/add_article.html', {'form': form})


class ArticleDetailsView(DetailView):
    model = Article
    template_name = 'articles/article_details.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = context['article']

        is_owner = article.user == self.request.user

        context['form'] = ArticleCommentForm()
        context['comments'] = article.articlecomment_set.all().order_by('date_posted')
        context['comments_count'] = article.articlecomment_set.count()
        context['is_owner'] = is_owner

        return context


class EditArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('news')
    template_name = 'articles/edit_article.html'


class DeleteArticleView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.delete()
        return redirect('news')


class CommentArticleView(LoginRequiredMixin, View):
    form_class = ArticleCommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            article = Article.objects.get(pk=self.kwargs['pk'])
            comment = ArticleComment(
                text=form.cleaned_data['text'],
                article=article,
                user=self.request.user,
            )
            comment.save()

            return redirect('article details', article.id)

        return redirect('article details', self.kwargs['pk'])


class DeleteArticleCommentView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs['pk'])
        comment = article.bookreview_set.filter(user_id=self.request.user.id)
        comment.delete()
        return redirect('book details', article.pk)
