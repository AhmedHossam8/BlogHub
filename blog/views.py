from django.shortcuts import render, redirect
from django.http import Http404
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, RegistrationForm, LoginForm, UserProfileForm
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.db.models import Q


# ------------------ VIEWS ------------------

def home(request):
    """Home page view with dynamic data"""
    
    published_posts = Post.objects.filter(status__iexact="published")

    total_posts = published_posts.count()

    total_authors = published_posts.values("author").distinct().count()

    categories = Category.objects.all()
    
    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        "site_name": "BlogHub",
        "tagline": "Your Platform for Sharing Ideas",
        "total_posts": total_posts,
        "total_authors": total_authors,
        "current_year": datetime.now().year,

        # Static homepage sections remain unchanged
        "featured_topics": ["Technology", "Design", "Travel", "Education", "Lifestyle"],
        "features": [
            {"icon": "✍️", "title": "Easy Publishing", "description": "Write and publish posts effortlessly"},
            {"icon": "🎨", "title": "Beautiful Design", "description": "Professional templates for your content"},
            {"icon": "👥", "title": "Engage Readers", "description": "Build your audience and community"},
            {"icon": "📊", "title": "Analytics", "description": "Track your post performance"},
        ],
        "is_featured_active": True,
        "spotlight_topic": "Web Development",

        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """About page view"""
    
    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        'company_name': 'BlogHub Team',
        'founded_year': 2025,
        'mission': 'Empowering writers to share their stories with the world',
        'team_size': 15,
        'values': ['Creativity', 'Community', 'Quality Content', 'Freedom of Expression'],
        'leaders': [
            {'name': 'Sarah Johnson', 'role': 'CEO'},
            {'name': 'Mike Chen', 'role': 'CTO'},
            {'name': 'Emma Rodriguez', 'role': 'Head of Content'},
        ],
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/about.html', context)


def contact(request):
    """
    Contact page with form submission
    GET: Show form
    POST: Process form submission
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields.')
        elif '@' not in email:
            messages.error(request, 'Please enter a valid email address.')
        else:
            # In real app: Send email, save to database, etc.
            print(f"Contact form submission:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            
            # Success message
            messages.success(request, f'Thank you {name}! We received your message and will respond soon.')
            
            # Redirect to avoid form resubmission
            return redirect('blog:contact')
    
    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    # GET request or after POST redirect
    context = {
        'email': 'contact@bloghub.com',
        'phone': '+1-800-BLOGHUB',
        'address': '123 Writer Street, Content City, CC 12345',
        'business_hours': 'Monday - Friday: 9AM - 6PM',
        'departments': [
            {'name': 'Editorial', 'email': 'editorial@bloghub.com'},
            {'name': 'Support', 'email': 'support@bloghub.com'},
            {'name': 'Partnerships', 'email': 'partners@bloghub.com'},
        ],
        'social_media': [
            {'platform': 'Facebook', 'link': 'facebook.com/bloghub'},
            {'platform': 'Twitter', 'link': 'twitter.com/bloghub'},
            {'platform': 'Instagram', 'link': 'instagram.com/bloghub'},
        ],
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/contact.html', context)


def posts(request):
    """All posts view with optional category filter"""
    posts_queryset = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts_queryset, 10)  # Show 10 posts per page
    page_number = request.GET.get('page') # /posts/?page=2
    posts = paginator.get_page(page_number)
    
    # Get featured posts
    featured_posts = Post.objects.filter(
        status=Post.Status.PUBLISHED,
        is_featured=True
    )[:3]
    
    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        'posts': posts,
        'featured_posts': featured_posts,
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/posts.html', context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status=Post.Status.PUBLISHED
    )
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get related posts (same category)
    related_posts = Post.objects.filter(
        category=post.category,
        status=Post.Status.PUBLISHED
    ).exclude(id=post.id)[:3]
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, category_name):
    """
    Display posts filtered by category
    
    URL: /category/technology/
    Shows only posts in that category
    """
    # Filter posts by category
    # force category_name to lower case for display
    # URL: /category/technology/ → category_name = "technology"
    # We need now to match: "technology" (lowercase)
    
    if category_name != category_name.lower():
        # Redirect to lowercase version
        return redirect('blog:category_posts', category_name=category_name.lower())
    
    category = get_object_or_404(Category, name__iexact=category_name)
    
    filtered_posts = Post.objects.filter(
        category=category,
        status=Post.Status.PUBLISHED
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()

    context = {
        'category_name': category.name,
        'posts': filtered_posts,
        'total_posts': filtered_posts.count(),
        'categories': categories,
        'authors': authors,
        'current_year': datetime.now().year,
        'site_name': 'BlogHub',
    }
    return render(request, 'blog/category_posts.html', context)


def search_posts(request):
    """
    Search posts by title or content
    
    URL: /search/?q=django
    Searches in post title and excerpt
    """
    # Get search query from URL parameters
    query = request.GET.get('q', '').strip()

    # Start with an empty queryset
    search_results = Post.objects.none()

    if query:
        search_results = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('author', 'category').prefetch_related('tags')
    else:
        # If no query: return all published posts
        search_results = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).select_related('author', 'category').prefetch_related('tags')

    context = {
        'query': query,
        'posts': search_results,
        'total_results': search_results.count(),
    }
    return render(request, 'blog/search_results.html', context)


def author_posts(request, author_name):
    """Display posts filtered by author.

    URL: /author/<author name>/
    Shows only posts written by this author.
    """

    # Normalize author name in URL
    if author_name != author_name.lower():
        return redirect('blog:author_posts', author_name=author_name.lower())

    # Get the author (case-insensitive)
    author = get_object_or_404(User, username__iexact=author_name)

    # Get the author's published posts
    filtered_posts = Post.objects.filter(
        author=author,
        status=Post.Status.PUBLISHED
    ).select_related('author', 'category').prefetch_related('tags')

    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()

    context = {
        'posts': filtered_posts,
        'total_posts': filtered_posts.count(),
        'author_name': author.username,
        'current_year': datetime.now().year,
        'site_name': 'BlogHub',
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/author_posts.html', context)


def featured_posts(request):
    """Featured posts view"""
    # Get featured + published posts from DB
    featured_posts = (
        Post.objects.filter(
            status=Post.Status.PUBLISHED,
            is_featured=True
        )
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-date")[:6]
    )

    # Get categories and authors for navbar
    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()

    context = {
        "posts_list": featured_posts,
        "site_name": "BlogHub",
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'blog/featured_posts.html', context)


# ------------------ CRUD ------------------


def post_list(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)\
        .select_related('author', 'category')\
        .prefetch_related('tags')

    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()

    context = {
        "posts": posts,
        "categories": categories,
        "authors": authors,
    }
    return render(request, "blog/posts.html", context)


def post_detail_fbv(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status=Post.Status.PUBLISHED
    )

    post.views_count += 1
    post.save(update_fields=['views_count'])

    comments = post.comments.filter(is_approved=True)

    related_posts = Post.objects.filter(
        category=post.category,
        status=Post.Status.PUBLISHED
    ).exclude(id=post.id)[:3]

    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()

    context = {
        "post": post,
        "related_posts": related_posts,
        "comments": comments,
        "categories": categories,
        "authors": authors,
    }
    return render(request, "blog/post_detail.html", context)


@login_required(login_url='blog:login')
def post_create(request):
    """Create a new blog post (login required)."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = Post.Status.PUBLISHED
            post.save()
            form.save_m2m()
            messages.success(request, 'Post created successfully!')
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm()

    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        "form": form,
        'categories': categories,
        'authors': authors,
    }
    return render(request, "blog/post_form.html", context)


@login_required(login_url='blog:login')
def post_update(request, slug):
    """Update a blog post (only author can update)."""
    post = get_object_or_404(Post, slug=slug)

    # Check if user is the post author
    if post.author != request.user:
        messages.error(request, "You can only edit your own posts.")
        return redirect("blog:post_detail", slug=post.slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        "form": form,
        "post": post,
        'categories': categories,
        'authors': authors,
    }
    return render(request, "blog/post_form.html", context)


@login_required(login_url='blog:login')
def post_delete(request, slug):
    """Delete a blog post (only author can delete)."""
    post = get_object_or_404(Post, slug=slug)

    # Check if user is the post author
    if post.author != request.user:
        messages.error(request, "You can only delete your own posts.")
        return redirect("blog:post_detail", slug=post.slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect("blog:posts")

    categories = Category.objects.all()
    authors = User.objects.filter(posts__status='published').distinct()
    
    context = {
        "post": post,
        'categories': categories,
        'authors': authors,
    }
    
    return render(request, "blog/post_confirm_delete.html", context)


# ================== AUTHENTICATION VIEWS (CBV) ==================


class RegisterView(CreateView):
    """User registration using CBV."""
    form_class = RegistrationForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('blog:login')
    
    def form_valid(self, form):
        """Save user and create profile."""
        response = super().form_valid(form)
        user = form.save()
        
        # Create UserProfile for new user
        from .models import UserProfile
        UserProfile.objects.create(user=user)
        
        # Show success message
        messages.success(
            self.request,
            f'Account created successfully! Please log in with your credentials.'
        )
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        authors = User.objects.filter(posts__status='published').distinct()
        context.update({
            'categories': categories,
            'authors': authors,
        })
        return context


class LoginView(LoginView):
    """User login using CBV."""
    template_name = 'blog/login.html'
    success_url = reverse_lazy('blog:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        authors = User.objects.filter(posts__status='published').distinct()
        context.update({
            'categories': categories,
            'authors': authors,
        })
        return context
    
    def form_valid(self, form):
        """Handle successful login."""
        messages.success(self.request, f'Welcome back, {form.cleaned_data.get("username")}!')
        return super().form_valid(form)


class LogoutView(View):
    """Custom logout view that handles both GET and POST requests."""
    
    def get(self, request, *args, **kwargs):
        """Handle GET requests for logout."""
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('blog:home')
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests for logout."""
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('blog:home')


class UserProfileUpdateView(UpdateView):
    """Update user profile information."""
    form_class = UserProfileForm
    template_name = 'blog/profile_form.html'
    success_url = reverse_lazy('blog:home')
    
    def get_object(self, queryset=None):
        """Get the logged-in user's profile."""
        if not self.request.user.is_authenticated:
            return redirect('blog:login')
        
        from .models import UserProfile
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        authors = User.objects.filter(posts__status='published').distinct()
        context.update({
            'categories': categories,
            'authors': authors,
            'profile_user': self.request.user,
        })
        return context
    
    def form_valid(self, form):
        """Handle successful profile update."""
        form.save()
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super().form_valid(form)
