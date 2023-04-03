from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('', views.Routes),
        
    path('user/password/reset/',PasswordResetView.as_view(),name='rest_password_reset'),
    path('user/password/reset/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    #TODO Auth
    path('rest-auth/google/', views.GoogleLogin.as_view()),
    path('auth/', include('dj_rest_auth.urls')),
    path('register', views.Register),

    #TODO Profile
    path('profile/<int:id>',views.GetProfile),
    path('profile/<int:id>/google',views.GoogleAddOrGetProfile),
    path('profile/add',views.AddProfile),
    path('profile/update', views.UpdateProfile),
    path('profile/<int:follow_id>/follow', views.ToogleProfileFollow),
    # path('profile/<int:mute_id>/mute', views.MuteProfile),
    
    #TODO Post
    path('post/add', views.AddPost),
    path('post/<int:id>', views.GetPost),
    path('post/<int:id>/delete', views.DeletePost),
    path('post/<int:id>/update', views.UpdatePost),
    path('post/filter', views.FilterPostText),
    path('post/most-liked', views.MostLikedPost),
    path('post/most-commented', views.MostCommentedPost),
    path('post/<int:post_id>/toggle', views.ToggleLikePost),
    path('post/<int:post_id>/answer', views.AnswerPost),
    path('answer/<int:comment_id>/delete', views.DeleteAnswer),

    #TODO News
    path('news/<int:id>', views.GetNews),
    path('news/add', views.AddNews),
    path('news/<int:id>/delete', views.DeleteNews),
    path('news/<int:id>/update', views.UpdateNews),
]
