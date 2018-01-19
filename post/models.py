from django.db import models
from django.utils.functional import cached_property
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=128)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()

    # @property把类的方法属性化，不需要加括号
    @property
    def tags(self):
        article_tags = Article_Tag.objects.filter(aid=self.id).only('tid')
        tid_list = [at.tid for at in article_tags]
        return Tag.objects.filter(id__in=tid_list)

   
    # 此处传进来的tags是最新更的tags
    def update_article_tags(self,tag_names):
# 第一种思路：
        # 取出要删除的关系的tid
        # need_del = []
        # for tag in self.tags:
        #     if tag.name not in tag_names:
        #         need_del.append(tag.id)
        #     else:
        #         # 需要保留的，删除掉了
        #         tag_names.remove(tag.name)

        # 删除旧的关系
        # articletags = Article_Tag.objects.filter(name__in=need_del)
        # for atag in articletags:
        #     atag.delete()

        # # 创建新的Tag和关系
        # Tag.creat_new_tags(tag_names,self.id)

# 第二种思路：
        old_tag_names = set(tag.name for tag in self.tags)
        new_tag_names = set(tag_names) - old_tag_names
        need_delete = old_tag_names - set(tag_names)

        # 删除旧的关系
        need_delete_tids = [t.id for t in Tag.objects.filter(name__in=need_delete).only('id')]
        articletags = Article_Tag.objects.filter(tid__in=need_delete_tids)
        for atag in articletags:
            atag.delete()

        # 创建新的关系
        Tag.creat_new_tags(new_tag_names,self.id)




class Comment(models.Model):
    aid = models.IntegerField()
    name = models.CharField(max_length=128,null=False,blank=False)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()


class Tag(models.Model):
    name = models.CharField(max_length=128,unique=True,null=False,blank=False)

    @classmethod
    def creat_new_tags(cls,tag_names,aid):
        # 创建Tags：
        # 取出已存在的tags
        exist_tags = cls.objects.filter(name__in=tag_names).only('name')
        # 取出已存在的tags 的name
        exists = [t.name for t in exist_tags]
        # 去除已存在的tags
        new_tags = set(tag_names) - set(exists)
        # 生成带创建的tag对象的列表
        new_tags = [cls(name=n) for n in new_tags]
        # 批量创建
        cls.objects.bulk_create(new_tags)

        # 建立与Article的关系：
        tags = cls.objects.filter(name__in=tag_names)
        for t in tags:
            Article_Tag.objects.update_or_create(aid=aid,tid=t.id)

        return tags

    @cached_property
    def articles(self):
        aid_list = [at.aid for at in ArticleTags.objects.filter(tid=self.id).only('aid')]
        return Article.objects.filter(id__in=aid_list)


class Article_Tag(models.Model):
    aid = models.IntegerField()
    tid = models.IntegerField()


