from django.urls import path

# from bbs.views import hello, list_article, detail_article, create_or_update_article
#
# urlpatterns = [
#     path('hello/<to>', hello),
#     path('article', list_article),
#     path('article/create/', create_or_update_article, {'article_id':None}),
#     path('article/<article_id>', detail_article),
#     path('article/<article_id>/update',create_or_update_article),
# ]

from bbs.views import  hello, ArticleCreateUpdateView, ArticleDetailView, ArticleListView

# as_view() 메소드의 역할 뷰클래스의 초기화와 핸들러를 반환하는 기능
urlpatterns = [
    path('hello/<to>', hello),
    path('article/', ArticleListView.as_view(), name="article"),
    path('article/create', ArticleCreateUpdateView.as_view(), name="article_craete"),
    path('article/<article_id>', ArticleDetailView.as_view(), name="article_detail"),
    path('article/<article_id>/update', ArticleCreateUpdateView.as_view(), name="article_update"),
]