# Library Management System (LMS)

A comprehensive Django-based Library Management System that provides complete book management, member administration, loan tracking, and fine calculation capabilities.

## 🚀 Features

### 📚 Book Management
- **Book Catalog**: Complete book inventory with title, author, category, and publication year
- **Copy Management**: Track total copies and available copies for each book
- **CRUD Operations**: Create, read, update, and delete book records
- **Book Search**: Easy book discovery and management

### 👥 Member Management
- **User Registration**: Self-registration system with member profile creation
- **Member Profiles**: Store member information including name, email, and phone
- **User Authentication**: Secure login/logout system with role-based access
- **Member Directory**: Complete member listing and management

### 📖 Loan Management
- **Book Borrowing**: Issue books to members with due dates
- **Return Tracking**: Monitor book returns and loan status
- **Loan History**: Complete loan records and history
- **Status Management**: Track borrowed and returned status

### 💰 Fine Management
- **Automatic Calculation**: Automatic fine calculation based on late returns
- **Fine Rate**: ₹20 per day for overdue books
- **Payment Tracking**: Track fine payment status
- **Fine History**: Complete fine records and management

### 🔐 Security & Access Control
- **Role-Based Access**: Admin-only access for management functions
- **User Dashboard**: Personalized dashboard for regular members
- **Admin Panel**: Full administrative control for staff
- **Authentication**: Secure user authentication system

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Authentication**: Django's built-in authentication system
- **Deployment**: Render.com ready
- **Dependencies**: See `requirements.txt`

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- PostgreSQL (for production)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd LMS
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
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@host:port/database_name
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
```

### 6. Run the Application
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`



## 🎯 Usage Guide

### For Administrators
1. **Login** with admin credentials
2. **Dashboard**: View overview of books, members, loans, and fines
3. **Book Management**: Add, edit, or remove books from the catalog
4. **Member Management**: Manage member accounts and information
5. **Loan Management**: Issue and track book loans
6. **Fine Management**: Monitor and manage overdue fines

### For Members
1. **Register** for a new account
2. **Login** to access personal dashboard
3. **View Loans**: Check current and past book loans
4. **View Fines**: Check any outstanding fines
5. **Profile Management**: Update personal information

## 🔧 Key Models

### Book Model
- Title, Author, Category, Publication Year
- Total copies and available copies tracking
- Automatic availability management

### Member Model
- User authentication integration
- Personal information (name, email, phone)
- One-to-one relationship with Django User

### Loan Model
- Book and member relationships
- Loan date, due date, and return date
- Status tracking (borrowed/returned)

### Fine Model
- Automatic fine calculation (₹20/day)
- Payment status tracking
- Loan and member relationships

## 🌐 API Endpoints

### Authentication
- `/login/` - User login
- `/logout/` - User logout
- `/register/` - User registration

### Dashboard
- `/` - Admin dashboard
- `/dashboard/` - User dashboard

### Book Management
- `/books/` - Book list
- `/books/all/` - Complete book list
- `/book/create/` - Add new book
- `/book/<id>/update/` - Edit book
- `/book/<id>/delete/` - Delete book

### Member Management
- `/members/` - Member list
- `/members/all/` - Complete member list
- `/member/create/` - Add new member
- `/member/<id>/edit/` - Edit member
- `/member/<id>/delete/` - Delete member

### Loan Management
- `/loans/` - Loan list
- `/loans/all/` - Complete loan list
- `/loan/create/` - Create new loan
- `/loan/<id>/edit/` - Edit loan
- `/loan/<id>/delete/` - Delete loan

### Fine Management
- `/fines/` - Fine list
- `/fines/all/` - Complete fine list
- `/fine/create/` - Create new fine
- `/fine/<id>/edit/` - Edit fine
- `/fine/<id>/delete/` - Delete fine

## 🚀 Deployment

### Render.com Deployment
1. Connect your GitHub repository to Render
2. Configure environment variables
3. Set build command: `pip install -r requirements.txt && python manage.py migrate`
4. Set start command: `gunicorn Book.wsgi:application`
5. Deploy!








