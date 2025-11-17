from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from .models import Category, Tag, Post, Comment

# Customize admin site branding
admin.site.site_header = 'Blog Administration'
admin.site.site_title = 'Blog Admin'
admin.site.index_title = 'Welcome to Blog Admin Panel'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    ordering = ['name']
    
    def post_count(self, obj):
        count = obj.posts.count()
        return format_html(
            '<span style="background-color: #007bff; color: white; '
            'padding: 2px 8px; border-radius: 10px;">{}</span>',
            count
        )
    post_count.short_description = 'Posts'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _post_count=Count('posts', distinct=True)
        )
        return queryset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    readonly_fields = ['created_at']
    ordering = ['name']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['author', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']
    can_delete = True
    show_change_link = True
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author_name',
        'category',
        'status_badge',
        'featured_icon',
        'views_count',
        'comment_count',
        'created_at',
    ]
    list_display_links = ['title']
    list_filter = [
        'status',
        'is_featured',
        'allow_comments',
        'category',
        ('created_at', admin.DateFieldListFilter),
    ]
    search_fields = [
        'title',
        'content',
        'excerpt',
        'author__username',
        'category__name',
    ]
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 25
    list_select_related = ['author', 'category']
    filter_horizontal = ['tags']  # Better UI for ManyToMany
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'views_count',
        'published_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author')
        }),
        ('Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Classification', {
            'fields': ('category', 'tags')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'allow_comments')
        }),
        ('Metadata', {
            'fields': (
                'views_count',
                'published_at',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',),
        }),
    )
    
    inlines = [CommentInline]
    
    actions = ['make_published', 'make_draft', 'feature_posts']
    
    # Custom display methods
    
    def author_name(self, obj):
        return obj.author.username
    author_name.short_description = 'Author'
    author_name.admin_order_field = 'author__username'
    
    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d',
            'published': '#28a745',
            'archived': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def featured_icon(self, obj):
        if obj.is_featured:
            return format_html('⭐')
        return format_html('<span style="opacity: 0.3;">☆</span>')
    featured_icon.short_description = '★'
    
    def comment_count(self, obj):
        count = obj.comments.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #007bff; color: white; '
                'padding: 2px 6px; border-radius: 10px; font-size: 11px;">{}</span>',
                count
            )
        return '0'
    comment_count.short_description = 'Comments'
    
    # Custom actions
    
    def make_published(self, request, queryset):
        for post in queryset:
            post.status = Post.Status.PUBLISHED
            if not post.published_at:
                post.published_at = timezone.now()
            post.save()
        
        count = queryset.count()
        self.message_user(
            request,
            f'{count} post(s) successfully published.'
        )
    make_published.short_description = 'Publish selected posts'
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status=Post.Status.DRAFT)
        self.message_user(
            request,
            f'{updated} post(s) set to draft.'
        )
    make_draft.short_description = 'Set to draft'
    
    def feature_posts(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            f'{updated} post(s) marked as featured.'
        )
    feature_posts.short_description = 'Mark as featured'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'post_title',
        'author_name',
        'content_preview',
        'approval_status',
        'created_at',
    ]
    list_display_links = ['id', 'content_preview']
    list_filter = [
        'is_approved',
        ('created_at', admin.DateFieldListFilter),
    ]
    search_fields = [
        'content',
        'author__username',
        'post__title',
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 50
    list_select_related = ['author', 'post']
    
    actions = ['approve_comments', 'unapprove_comments']
    
    # Custom display methods
    
    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Post'
    post_title.admin_order_field = 'post__title'
    
    def author_name(self, obj):
        return obj.author.username
    author_name.short_description = 'Author'
    author_name.admin_order_field = 'author__username'
    
    def content_preview(self, obj):
        if len(obj.content) > 50:
            return f'{obj.content[:50]}...'
        return obj.content
    content_preview.short_description = 'Comment'
    
    def approval_status(self, obj):
        if obj.is_approved:
            return format_html(
                '<span style="color: green;">✓ Approved</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Pending</span>'
        )
    approval_status.short_description = 'Status'
    
    # Custom actions
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated} comment(s) approved.'
        )
    approve_comments.short_description = 'Approve selected comments'
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated} comment(s) unapproved.'
        )
    unapprove_comments.short_description = 'Unapprove selected comments'