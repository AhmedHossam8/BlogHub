from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # --- Authentication Routes (CBV) ---
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),

    # --- CRUD Function-Based Views ---
    path('posts/', views.post_list, name='posts'),  # list all posts
    path('posts/create/', views.post_create, name='post_create'),  # create new post
    path('posts/<slug:slug>/', views.post_detail_fbv, name='post_detail'),  # post detail
    path('posts/<slug:slug>/update/', views.post_update, name='post_update'),  # update post
    path('posts/<slug:slug>/delete/', views.post_delete, name='post_delete'),  # delete post

    # --- Filter Views ---
    path('category/<str:category_name>/', views.category_posts, name='category_posts'),
    path('author/<str:author_name>/', views.author_posts, name='author_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('featured-posts/', views.featured_posts, name='featured_posts'),
]