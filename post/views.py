from django.shortcuts import render, redirect

# Create your views here.
from post.models import Article, Comment,Tag,Article_Tag
from math import ceil
from django.core.cache import cache
from redis import Redis
from post.helper import page_cache,record_click
from post.helper import get_top_n_articles,statistic
from user.helper import permit
import os
from django.conf import settings
from django.http import HttpResponse

def upfile(request):
    return render(request,'upfile.html')

def savefile(request):
    f = request.FILES['file']
    filePath = os.path.join(settings.MEDIA_ROOT,f.name)
    with open(filePath,'wb') as fp:
        for info in f.chunks():
            fp.write(info)
    return render(request,'info.html')


@page_cache(1)
def home(request):

# 获取总页码数
    count = Article.objects.count()
    pages = ceil(count/2)
# 获取page
    page = int(request.GET.get('page',1))
    page = 0 if page < 1 or page >= (pages+1) else (page - 1)

    start = page * 2
    end = start + 2

    articles = Article.objects.all()[start:end]

    tags = Tag.objects.all()



    # 选出top10
    top10 = get_top_n_articles(10)


    return render(request,'home.html',{'articles':articles,'page':page,'pages':range(pages),'top10':top10,'tags':tags})


@statistic
@page_cache(1)
@permit('user')
def article(request):

    aid = int(request.GET.get('aid',1))

    # key = 'article-%s'%aid
    # article = cache.get(key)
    # if article is None:
    #     article = Article.objects.get(id=aid)
    #     cache.set(key,article)
    
    article = Article.objects.get(id=aid)
    comments = Comment.objects.filter(aid=aid)

    # 记录文章点击量
    post_views = record_click(aid)

    return render(request,'article.html',{'article':article,'comments':comments,'post_views':post_views,'tags':article.tags})


@permit('user')
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        article = Article.objects.create(title=title, content=content)

        tags = request.POST.get('tags','')
        if tags:
            tags = [t.strip() for t in tags.split('，')]
            Tag.creat_new_tags(tags,article.id)


        return redirect('/post/article/?aid=%s' % article.id)
    else:
        return render(request, 'create.html')

@permit('user')
def editor(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()

        # 创建或更新或删除tags
        tags = request.POST.get('tags','')
        if tags:
            tag_names = [t.strip() for t in tags.split('，')]
            article.update_article_tags(tag_names)

        return redirect('/post/article/?aid=%s' % article.id)
    else:
        aid = int(request.GET.get('aid', 0))
        article = Article.objects.get(id=aid)
        return render(request, 'editor.html', {'article': article,'tags':article.tags})

@permit('user')
def comment(request):
    if request.method == 'POST':
        # form = CommentForm(request.POST)
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        Comment.objects.create(name=name, content=content, aid=aid)
        return redirect('/post/article/?aid=%s' % aid)
    return redirect('/post/home/')
#

def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        articles = Article.objects.filter(content__contains=keyword)
        return render(request, 'home.html', {'articles': articles})

@permit('user')
def delete(request):
    # pass
    aid = int(request.GET.get('aid',1))

    article = Article.objects.get(id=aid)
    article.delete()
    
    return redirect('/post/home/')

def tag(request):
    # articles = Tag.articles
    tid = request.GET.get('tid')
    aid_list = [at.aid for at in Article_Tag.objects.filter(tid=tid).only('aid')]
    articles = Article.objects.filter(id__in=aid_list)
    return render(request,'tag.html',{'articles':articles})


