from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# ===================================== 함수형 기반 뷰 ======================================
from django.views.generic.detail import SingleObjectMixin

from bbs.models import Article


def hello(request, to):
    return HttpResponse('Hello {}.'.format(to))

def list_article(request):    #목록보기
    return HttpResponse('list')

def detail_article(request, article_id):
    return HttpResponse('detail {}'.format(article_id))

def create_or_update_article(request, article_id):
    if article_id: #수정하기
        if request.method == "GET":
            return HttpResponse('update {}'.format(article_id))
        elif request.method == "POST":
            return do_create_article(request)
        else:HttpResponseNotAllowed(['GET', 'POST'])
    else:
        if request.method == "GET":
            return HttpResponse('create')
        elif request.method == "POST":
            return do_update_article(request)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])



def do_create_article(request):
    return HttpResponse(request.POST)

def do_update_article(request):
    return HttpResponse(request.POST)

#----------------------------------- 클레스 기반 뷰 -----------------------------

# 게시글 목록 가기
class ArticleListView(TemplateView, SingleObjectMixin):
    template_name = 'article_list.html'
    quryset = Article.objects.all()

    def get(self, request, *arg, **kwargs):
        # 템플릿에 전달할 데이터
        ctx = {
            "articles":self.quryset
        }
        return self.render_to_response(ctx)

# 게시글 상세
class ArticleDetailView(TemplateView):
    template_name = 'article_detail.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'    # 검색데이터의 primary key 를 전달 받음

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset      # queryset 파라미터 초기화
        pk = self.kwargs.get(self.pk_url_kwargs)  # pk는 모델에서 정의된 pk값, 즉 모델의 id
        article = queryset.filter(pk=pk).first()     # pk 로 검색된 데이터가 있다면 그중 첫번쨰 없다면 None

        if not article:
            raise Http404('inbalid pk')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if not article:
            raise Http404('invail artcle_id') # 검색된 아이디가 없습니다.
        ctx = {
            "article": article
        }
        return self.render_to_response(ctx)

# 게시글 추가, 수정
@method_decorator(csrf_exempt, name='dispatch') # 모든 핸들러 예외처리
class ArticleCreateUpdateView(TemplateView):
    template_name = 'article_update.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'
    # 화면 요청

    def get_object(self, queryset= None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        article = queryset.filter(pk=pk).first()

        if pk and not article:
            raise Http404('invaild pk')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        if not article:
            raise Http404('invalid article_id')
        ctx = {
            'article':article
        }
        return self.render_to_response(ctx)

    # post 요청청
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        post_data = {key: request.POST.get(key) for key in ('title', 'content', 'author')}
        for key in post_data:
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tag='danger')
                # raise Http404('no data for {}'.format(key))
        if len(messages.get_messages(request)) == 0:

            if action == 'create':
                article = Article.obejcts.create(**post_data)
                messages.success(self.request, '게시글이 저장되었습니다.')
                # article = Article.objects.create(title=post_data.keys('title'), content=post_data.keys('content'), author=post_data.keys('author'))
            elif action == 'update':
                article = self.get_object()
                for key, value in post_data.items():
                    setattr(article, key, value)
                article.save()
                messages.success(self.request, '게시글이 저장되었습니다.')
            else:
                messages.error(self.request, '알수 없는 요청입니다.', extr_tags="danger")

            return HttpResponseRedirect('/article/')
        ctx = {
            'article' : self.get_object() if action == 'update' else None
        }
        return self.render_to_response(ctx)

