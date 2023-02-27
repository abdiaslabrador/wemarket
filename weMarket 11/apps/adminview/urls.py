from django.conf.urls import url, include
from apps.adminview.views import (
                                    searchClasif, admin_given, delete_bill,
                                    index_admin,  cuadricula,
                                    article, add_article, edit_article, delete_article,
                                    clasification, add_clasification, edit_clasificacion, delete_clasificacion,
                                    order_by_list, order_by_cuadr,
                                    sells, design, users, searchBar, log_required

                                 )
from apps.adminview.views import (  
                                    preload_image, edit_member, add_member, 
                                    save_page, delete_member, save_design, 
                                    searchUser, edit_design, edit_user, 
                                    preload_carrousel, select_template, save_template, 
                                    choosedesign, select_design, save_design, 
                                    user_delete, advice_user,
                                    without_stock, without_stock_cuadricula,
                                  )
from django.urls import path


app_name = 'adminview'

urlpatterns = [
    url(r'^$', index_admin, name="adminview"),
    url(r'^clasification', clasification, name="clasification"),
    url(r'^category/edit/(?P<id_category>\d+)/$', edit_clasificacion, name="edit_clasificacion"),
    url(r'^product/edit/(?P<id_article>\d+)/$', edit_article, name="edit_article"),
    url(r'^member/edit/(?P<id_member>\d+)/$', edit_member, name="edit_member"),
    url(r'^add_clasification', add_clasification, name="add_clasification"),
    url(r'^article', article, name="article"),
    url(r'^add_article', add_article, name="add_article"),
    url(r'^memberadd', add_member, name="add_member"),
    url(r'^delete_clasification/(?P<id_category>\d+)/$', delete_clasificacion, name='delete_clasificacion'),
    url(r'^delete_article/(?P<id_article>\d+)/$', delete_article, name='delete_article'),
    url(r'^order_by_list/(?P<id_category>\d+)/$', order_by_list, name='order_by_list'),#ordenar por lista
    url(r'^order_by_cuadr/(?P<id_category>\d+)/$', order_by_cuadr, name='order_by_cuadr'),
    url(r'^cuadricula', cuadricula, name="cuadricula"),
    path('sells/', sells, name='sells'),
    path('admin_given/<int:id_bill>/', admin_given, name='admin_given'),
    path('delete_bill/<int:id_bill>/', delete_bill, name='delete_bill'),
    url(r'^design', design, name="design"),
    url(r'^users', users, name="users"),
    url(r'^search/ajax(?P<option>\d+)/$', searchBar, name="searchBar"),
    url(r'^ajax3', searchClasif, name="searchClasif"),#botón de búsqueda
    url(r'^buscar/searchAjax/$', searchBar),
    url(r'^choosedesign', choosedesign, name="choosedesign"),
    path('template/<int:id_template>/', select_template, name='select_template'),
    path('Sdesign/<int:id_design>/', select_design, name='select_design'),
    path('save_template/<int:id_template>/', save_template, name='save_template'),
    path('sveDesg/<int:id_design>/', save_design, name='save_design'),
    path('preload/<int:pk>/', preload_image, name='preload_image'),  #esto muestra solo la imagen
    path('userdelete/<int:id_user>/<int:actual_user>/', user_delete, name='user_delete'),
    path('advice_user/', advice_user, name='advice_user'),
    path('useredition/<int:id_user>/<int:active_user>/', edit_user, name='edit_user'),
    path('usSearch/', searchUser, name='searchUser'),
    path('desEdit/', edit_design, name='edit_design'),
    path('carrousel/<int:option>/<int:pk>/', preload_carrousel, name='preload_carrousel'),
    path('membdel/<int:id_member>/', delete_member, name='delete_member'),
    path('savepage/', save_page, name='save_page'),
    path('without_stock/', without_stock, name='without_stock'),
    path('cuadriwstock/', without_stock_cuadricula, name='without_stock_cuadricula'),
    path('log_required/', log_required, name='log_required')
]