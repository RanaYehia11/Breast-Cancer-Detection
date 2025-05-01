from django.urls import path ,include
from .import views 
from .views import user_logout

urlpatterns = [

    path('',views.index, name="login"),
    path('logout/', user_logout, name='logout'),

]
