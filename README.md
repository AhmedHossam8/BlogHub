# 📝 BlogHub - Django Blog Platform

A comprehensive blog management system built with Django, featuring user authentication, post management, and dynamic content filtering.

## ✨ Features

### User Management
- **User Registration & Authentication**: Secure user registration with email validation
- **Profile Management**: Users can create and update their profiles with avatars, bio, website, and location
- **Role-Based Access Control**: Admin interface for managing users and content

### Blog Functionality
- **CRUD Operations**: Create, Read, Update, and Delete blog posts
- **Rich Content Management**: Support for titles, excerpts, and full content
- **Post Categorization**: Organize posts using categories and tags
- **Draft System**: Save posts as drafts before publishing
- **Featured Posts**: Highlight important content on the homepage
- **Post Status Management**: Draft, Published, and Archived states

### Content Organization
- **Categories**: Organize posts into logical categories
- **Tags**: Multi-tag support for flexible content organization
- **Search Functionality**: Search posts by title, excerpt, and category
- **Filtering**: Filter posts by category, author, and featured status

### Comments System
- **Comment Moderation**: Approve or reject comments before they appear
- **Threaded Comments**: Organized discussion on blog posts
- **User-Specific Comments**: Track comment authors

### Admin Panel
- **Comprehensive Dashboard**: Manage all aspects of the blog
- **Bulk Actions**: Publish, archive, or feature multiple posts at once
- **Rich Analytics**: View post statistics, comment counts, and view counts
- **Custom Admin Interface**: Enhanced Django admin with custom styling and features

## 🛠️ Technologies Used

- **Backend**: Django 5.2.8
- **Database**: PostgreSQL
- **Frontend**: Django Templates, Bootstrap 4.0
- **Authentication**: Django's built-in authentication system
- **Environment Management**: python-decouple

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/AhmedHossam8/BlogHub.git
cd bloghub
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django psycopg2-binary python-decouple
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=bloghub_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Set Up PostgreSQL Database
```bash
# Log into PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE bloghub_db;

# Create user and grant privileges
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE bloghub_db TO your_db_user;
\q
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 📁 Project Structure

```
bloghub/
├── blog/                      # Main blog application
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   └── blog/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── posts.html
│   │       ├── post_detail.html
│   │       ├── post_form.html
│   │       ├── login.html
│   │       ├── register.html
│   │       └── ...
│   ├── admin.py              # Admin panel configuration
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── forms.py              # Form classes
│   └── urls.py               # URL routing
├── bloghub/                   # Project configuration
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI configuration
├── static/                    # Static files (CSS, JS)
│   ├── css/
│   │   └── bootstrap.min.css
│   └── js/
│       └── bootstrap.bundle.min.js
├── manage.py                  # Django management script
├── .env                       # Environment variables (create this)
└── .gitignore                # Git ignore file
```

## 🎯 Usage

### Admin Panel
Access the admin panel at `http://127.0.0.1:8000/admin/`

**Features:**
- Manage posts, categories, tags, and comments
- Approve or reject comments
- Publish or archive posts in bulk
- View post statistics and analytics
- Manage user profiles

### User Features
- **Register**: Create a new account at `/register/`
- **Login**: Access your account at `/login/`
- **Create Post**: Write new blog posts at `/posts/create/`
- **View Posts**: Browse all posts at `/posts/`
- **Search**: Use the search bar to find specific posts
- **Filter by Category**: Click on categories to view related posts
- **Filter by Author**: View posts by specific authors

## 🗄️ Database Models

### Post
- Title, slug, excerpt, content
- Status (draft, published, archived)
- Featured flag
- Category and tags
- Author relationship
- View count and timestamps

### Category
- Name, slug, description
- Timestamp

### Tag
- Name, slug
- Timestamp

### Comment
- Content
- Approval status
- Author and post relationships
- Timestamps

### UserProfile
- Bio, avatar, website, location
- One-to-one relationship with User
- Timestamps

## 🔐 Security Features

- CSRF protection enabled
- Password validation and hashing
- SQL injection protection via ORM
- XSS protection through template escaping
- Authentication required for sensitive operations
- Permission-based access control

## 🎨 Customization

### Adding New Categories
1. Go to admin panel → Categories → Add Category
2. Fill in name and description
3. Slug will be auto-generated

### Creating Custom Templates
1. Navigate to `blog/templates/blog/`
2. Create or modify HTML files
3. Extend `base.html` for consistent layout

### Styling
- Bootstrap 4.0 is included in `static/css/`
- Custom styles can be added to templates or create separate CSS files

## 📝 Common Tasks

### Create Sample Data
```bash
python manage.py shell
```
```python
from blog.models import Category, Tag
Category.objects.create(name="Technology", description="Tech articles")
Tag.objects.create(name="Django")
```

### Clear Database
```bash
python manage.py flush
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## 🐛 Troubleshooting

**Database Connection Error:**
- Check PostgreSQL is running
- Verify `.env` credentials
- Ensure database exists

**Static Files Not Loading:**
- Run `python manage.py collectstatic`
- Check `STATIC_URL` in settings.py

**Migration Issues:**
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📦 Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS` in `settings.py`
3. Set up a production database
4. Configure static files serving
5. Use a production WSGI server (Gunicorn)
6. Set up HTTPS with SSL certificate

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Ahmed Hossam Emara

## 📧 Contact

For questions or support, please contact [ahmedhossamemara8@gmail.com]

---

**Note:** Remember to never commit your `.env` file to version control. It's already included in `.gitignore`.
