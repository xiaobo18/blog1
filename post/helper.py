
#coding:utf-8
import logging
from django.core.cache import cache
from post.models import Article, Comment
from redis import Redis
from post.models import Article

r = Redis(host='127.0.0.1',port=6379,db=1)
logger = logging.getLogger('statistic')

# 可以添加参数的装饰器(timeout是设定的缓存时间)
def page_cache(timeout):
    def wrap1(view_func):
        # 页面缓存
        def wrap2(request,*args,**kwargs):
            # 从缓存获取response
            key = 'PAGES-%s'% request.get_full_path()
            response = cache.get(key)
            # 如果有-》直接返回
            if response is not None:
                print('return from cache')
                return response
            else:
                # 如果没有 -》执行view函数
                response = view_func(request,*args,**kwargs)
                print('return from view_func')
                # 将结果添加缓存
                cache.set(key,response,timeout)
                return response
        return wrap2
    return wrap1

def record_click(article_id,count=1):
    # 记录文章点击量
    # r.zincrby('Article_clicks',article_id,count)
    num = r.zincrby('Article-clicks',article_id,count)
    return num
    # pass
'''
ZADD key score member [[score member] [score member] ...]
将一个或多个 member 元素及其 score 值加入到有序集 key 当中。

ZINCRBY key increment member
为有序集 key 的成员 member 的 score 值加上增量 increment 。
当 key 不存在，或 member 不是 key 的成员时， ZINCRBY key increment member 等同于 ZADD key increment member 

ZREVRANGE key start stop [WITHSCORES]
返回有序集 key 中，指定区间内的成员。
其中成员的位置按 score 值递减(从大到小)来排列。

'''

def get_top_n_articles(number):
# article_clicks格式：
    # [(b'3',123.0),
    # (b'3',123.0),
    # (b'3',123.0),
    # ......

    # ]

    # 获取TopN的文章
    article_clicks = r.zrevrange('Article-clicks',0,number,withscores=True)

    # article_clicks 列表推导式拆解过程
    # article_clicks_data = []
    # for aid, click in article_clicks:
    #     aid, click = int(aid), int(click)
    #     article_clicks_data.append([aid, click])

    # 数据类型转换
    article_clicks1 = [[int(aid),int(click)] for aid,click in article_clicks]
    # Article.objects.in_bulk(aid for aid, _ in article-clicks)
    print(article_clicks1)
    # 获取文章id列表
    aid_list = [d[0] for d in article_clicks1]
    # 根据文章的id列表，批量提取文章
    articles = Article.objects.in_bulk(aid_list)
    # print(articles)

# 转换aid为Article的实例
    for data in article_clicks1:
        # print(data[0] )
        # print('**********************1')
        aid = data[0]
        data[0] = articles[aid]
        # print(data[0])
        # print('----------------------2')
        # articles[aid]意思是根据aid取出这篇文章

# 返回的数据格式：
 # [
 #    [Article(6),132],
    # [Article(6),132],
    # [Article(6),132],
    # ......

    # ]

    return article_clicks1

def statistic(func):
    def wrap(request,*args,**kwargs):
        response = func(request,*args,**kwargs)

        if response.status_code == 200:
            ip = request.META['REMOTE_ADDR']
            aid = int(request.GET.get('aid',1))
            logger.info('%s   %s'%(ip,aid))

        return response
    return wrap








