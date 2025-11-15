from django.shortcuts import render, redirect
from django.http import Http404
from datetime import datetime
from django.contrib import messages

# Sample post data (will later come from DB)
all_posts = [
    {
        'id': 1,
        'title': 'Getting Started with Django',
        'author': 'Sarah Johnson',
        'category': 'Technology',
        'excerpt': 'Learn the fundamentals of Django development',
        'content': 'Django is a powerful web framework that makes building web applications fast and easy. In this guide, we explore the fundamentals of Django development.',
        'tags': ['Django', 'Python', 'Web Development', 'Tutorial'],
        'published': True,
        'date': '2025-01-15',
        'reading_time': '8 min',
        'views': 1250
    },
    {
        'id': 2,
        'title': 'Mastering CSS Grid Layout',
        'author': 'Mike Chen',
        'category': 'Design',
        'excerpt': 'CSS Grid revolutionized responsive design',
        'content': 'CSS Grid is a revolutionary layout system that changed how we build responsive designs. Learn how to create flexible layouts.',
        'tags': ['CSS', 'Design', 'Frontend', 'Grid'],
        'published': True,
        'date': '2025-01-20',
        'reading_time': '6 min',
        'views': 890
    },
    {
        'id': 3,
        'title': 'Traveling Through Southeast Asia',
        'author': 'Emma Rodriguez',
        'category': 'Travel',
        'excerpt': 'Discover hidden gems of Southeast Asia',
        'content': 'Discover the hidden gems of Southeast Asia with our comprehensive travel guide. From bustling cities to tranquil beaches.',
        'tags': ['Travel', 'Asia', 'Adventure', 'Culture'],
        'published': True,
        'date': '2025-01-25',
        'reading_time': '10 min',
        'views': 2100
    },
    {
        'id': 4,
        'title': 'Understanding Machine Learning Basics',
        'author': 'Dr. James Wilson',
        'category': 'Education',
        'excerpt': 'Machine learning concepts demystified',
        'content': 'Machine learning demystified. Learn the fundamental concepts and algorithms that power modern AI applications.',
        'tags': ['AI', 'Machine Learning', 'Education', 'Technology'],
        'published': False,
        'date': '2025-01-28',
        'reading_time': '12 min',
        'views': 0
    },
    {
        'id': 5,
        'title': 'Top 10 Photography Tips',
        'author': 'Lisa Anderson',
        'category': 'Photography',
        'excerpt': 'Transform your photography skills',
        'content': 'Transform your photography skills with these essential tips. From composition to lighting, master the basics.',
        'tags': ['Photography', 'Tutorial', 'Beginner', 'Tips'],
        'published': True,
        'date': '2025-02-01',
        'reading_time': '7 min',
        'views': 1500
    },
    {
        'id': 6,
        'title': 'Building REST APIs with Django',
        'author': 'Sarah Johnson',
        'category': 'Technology',
        'excerpt': 'Create powerful REST APIs using Django REST Framework',
        'content': 'Learn to build scalable REST APIs using Django REST Framework, with examples and best practices.',
        'tags': ['Django', 'API', 'Backend', 'REST'],
        'published': True,
        'date': '2025-02-05',
        'reading_time': '15 min',
        'views': 980
    },
    {
        'id': 7,
        'title': 'Minimalist Interior Design Trends',
        'author': 'Mike Chen',
        'category': 'Design',
        'excerpt': 'Less is more in modern interior design',
        'content': 'Explore minimalist interior design trends for modern living spaces and learn how to declutter elegantly.',
        'tags': ['Design', 'Interior', 'Minimalist', 'Trends'],
        'published': False,
        'date': '2025-02-08',
        'reading_time': '5 min',
        'views': 0
    },
    {
        'id': 8,
        'title': 'Healthy Meal Prep for Busy Professionals',
        'author': 'Emma Rodriguez',
        'category': 'Health',
        'excerpt': 'Save time and eat healthy with these meal prep tips',
        'content': 'Save time and eat healthy with meal prep strategies, recipes, and planning tips for busy professionals.',
        'tags': ['Health', 'Meal Prep', 'Nutrition', 'Wellness'],
        'published': True,
        'date': '2025-02-10',
        'reading_time': '9 min',
        'views': 670
    },
]


# ------------------ VIEWS ------------------

def home(request):
    """Home page view with dynamic data"""
    categories = sorted(set(post['category'] for post in all_posts))
    context = {
        'site_name': 'BlogHub',
        'tagline': 'Your Platform for Sharing Ideas',
        'total_posts': len(all_posts),
        'total_authors': len(set(post['author'] for post in all_posts)),
        'current_year': datetime.now().year,
        'featured_topics': ['Technology', 'Design', 'Travel', 'Education', 'Lifestyle'],
        'features': [
            {'icon': '✍️', 'title': 'Easy Publishing', 'description': 'Write and publish posts effortlessly'},
            {'icon': '🎨', 'title': 'Beautiful Design', 'description': 'Professional templates for your content'},
            {'icon': '👥', 'title': 'Engage Readers', 'description': 'Build your audience and community'},
            {'icon': '📊', 'title': 'Analytics', 'description': 'Track your post performance'},
        ],
        'is_featured_active': True,
        'spotlight_topic': 'Web Development',
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    """About page view"""
    categories = sorted(set(post['category'] for post in all_posts))
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
        ]
    }
    return render(request, 'blog/contact.html', context)


def posts(request):
    """All posts view with optional category filter"""
    selected_category = request.GET.get('category', '')  # empty string if none selected
    
    if selected_category:
        posts_list = [p for p in all_posts if p['category'].lower() == selected_category.lower()]
    else:
        posts_list = all_posts
    
    categories = sorted(set(post['category'] for post in all_posts))
    
    context = {
        "posts_list": posts_list,
        "categories": categories,
        "selected_category": selected_category,
        "page_title": "All Posts" if not selected_category else f"Posts in {selected_category}",
        'categories': categories,
    }
    return render(request, 'blog/posts.html', context)


def post_detail(request, post_id):
    try:
        post = next(p for p in all_posts if p['id'] == post_id)
    except StopIteration:
        raise Http404("Post not found")
    
    categories = sorted(set(p['category'] for p in all_posts))
    
    context = {
        'post': post,
        'tags': post.get('tags', []),
        'categories': categories,
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
    
    filtered_posts = [
        post for post in all_posts
        if post['category'].lower() == category_name
    ]
    
    categories = sorted(set(post['category'] for post in all_posts))
    
    # On Day 3 with database, this becomes:
    # filtered_posts = Post.objects.filter(category__iexact=category_name)
    
    context = {
        'category_name': category_name.title(),
        'posts': filtered_posts,
        'total_posts': len(filtered_posts),
        'categories': categories,
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
    query = request.GET.get('q', '')  # Default to empty string if no query
    
    # Search posts if query exists
    if not query:
        # If no query, return all posts
        search_results = all_posts
    else:
        search_results = [
            post for post in all_posts
            if query.lower() in post['title'].lower() or
            query.lower() in post['excerpt'].lower() or
            query.lower() in post['category'].lower()
        ]
    
    context = {
        'query': query,
        'posts': search_results,
        'total_results': len(search_results),
    }
    return render(request, 'blog/search_results.html', context)


def author_posts(request, author_name):
    """Display posts filtered by author.

    URL: /author/<author name>/
    Shows only posts written by this author.
    """

    # Normalize request to lowercase author name and redirect if necessary.
    if author_name != author_name.lower():
        return redirect('blog:author_posts', author_name=author_name.lower())

    # Filter posts by author (case-insensitive match)
    filtered_posts = [
        post for post in all_posts
        if post['author'].lower() == author_name
    ]

    # On Day 3 with database, this becomes:
    # filtered_posts = Post.objects.filter(author__iexact=author_name)

    # Include categories so the navbar in base.html can render correctly
    categories = sorted(set(p['category'] for p in all_posts))

    context = {
        'posts': filtered_posts,
        'total_posts': len(filtered_posts),
        'current_year': datetime.now().year,
        'site_name': 'BlogHub',
        'categories': categories,
    }
    return render(request, 'blog/author_posts.html', context)


def featured_posts(request):
    """Featured posts view"""
    posts_list = all_posts
    reversed_posts_list = sorted(posts_list, key=lambda x: x['date'], reverse=True)
    featured_posts = [post for post in reversed_posts_list if post['published']]
    for post in featured_posts:
        post['is_featured'] = True
    
    featured_posts = featured_posts[:6]
    
    context = {
        "posts_list": featured_posts,
        'site_name': 'BlogHub',
    }
    return render(request, 'blog/featured_posts.html', context)