
from django.contrib import admin
from django.urls import path ,include
from django.shortcuts import render
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('signup/', include('signup.urls')),
    path("ai/",include ("aiModel.urls")),
    path('home/', lambda request: render(request, 'pages/home.html'), name="home"),
    path('donation/', lambda request: render(request, 'pages/donation.html'), name="donation"),
    path('selfExam/',lambda request:render(request,'pages/selfExam.html'),name='selfExam'),
    path('faq/',lambda request:render(request,'pages/faq.html'),name='faq'),
   
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="pages/password_reset.html"), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="pages/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="pages/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="pages/password_reset_complete.html"), name="password_reset_complete"),



    
]


