from django.urls import path
# from .views import index, detail, answer_create
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:id>/<int:comment_id>/', views.detail, name = "detail"),
    path('comment/create/<str:id>/<int:num>', views.comment_create, name='comment_create'),
    path('comment/modify/<str:id>/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<str:id>/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    #path('camping_detail/', views.camping_detail, name='camping_detail'),   
    path('db/', views.db, name='db'),
    path('receive_data/', views.receive_data, name='receive_data'),

    path('answer/create/<str:id>/<int:comment_id>/', views.answer_create, name='answer_create'),
    path('answer/modify/<str:id>/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<str:id>/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    
    path('vote/comment/<str:id>/<int:comment_id>', views.vote_comment, name = "vote_comment"),
    path('vote/answer/<str:id>/<int:answer_id>', views.vote_answer, name = "vote_answer"),
    
    path('location/', views.location, name='location'),
    path('location/<str:id>/', views.location_detail, name='location_detail'),
    path('camping_detail/<str:id>/<int:num>', views.camping_detail, name='camping_detail'), 

    path('search/', views.search, name="search"),
    path('search/<str:radio>/<str:search>', views.search_val, name="search_val"),
]
