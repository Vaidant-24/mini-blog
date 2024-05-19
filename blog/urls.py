from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('signup/',views.user_signup,name='signup'),
    path('addpost/',views.add_post,name='add_post'),
    path('updatepost/<int:id>',views.update_post,name='update_post'),
    path('deletepost/<int:id>',views.delete_post,name='delete_post'),
]
