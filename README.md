"# BlogApi_training" 

A RESTful API for managing a blog platform, built using Django and Django REST Framework. This API allows users to create, read, update, and delete blog posts, categories, and authors.

## Features

- User authentication and authorization
- Create, retrieve, update, and delete blog posts
- Categorize posts and retrieve posts by category
- Validation for blog content length, Flesch Reading Ease score, and forbidden words
- Plagiarism check based on content similarity
- Draft management for blog posts

## Tech Stack

- Django >= 4.0
- Django REST Framework >= 3.12
- PostgreSQL or MySQL (or SQLite)
- textstat for readability analysis
- Python 3.x

## Installation
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

pip install -r requirements.txt

### Prerequisites

Make sure you have Python 3.x and pip installed on your machine.

API Endpoints
POST /api/blogs/createauthor/ - Create a new author
POST /api/blogs/createcategory/ - Create category
GET /api/popular-category/ - List popular categories
GET /api/popular-category/ - List popular categories
GET /api/top-authors/ - List top authors
POST /api/blogs/create/ - Create a new blog post
GET /api/blogs/ - List all blog posts
GET /api/blogs/drafts/ - List all drafts
GET /api/blogs/drafts/ - List all draft blog posts
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
