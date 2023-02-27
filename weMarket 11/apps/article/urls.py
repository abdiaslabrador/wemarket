from django.urls import path, include

from apps.article.views import show_article, delete_comment

app_name = 'article'

urlpatterns = [
    path('<int:id_article>/', show_article, name="show_article"),
    path('delcomment/<int:id_article>/<int:id_comment>', delete_comment, name="delete_comment"),
]