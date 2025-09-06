# FinTrack – Personal Finance & Expense Tracker

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive personal finance management web application built with Python Flask that helps users track income, expenses, and analyze spending patterns with beautiful visualizations and export capabilities.

## 🚀 Live Demo

**Access the application:** http://your-server-ip:5000

*Default login credentials (if pre-populated):*
- Username: `demo`
- Password: `password`

## ✨ Features

### 📊 Core Functionality
- **User Authentication** - Secure registration and login system
- **Transaction Management** - Full CRUD operations for income and expenses
- **Categorized Tracking** - Organized by Food, Rent, Travel, Shopping, Utilities, Entertainment, Salary, Freelance, etc.
- **Real-time Dashboard** - Financial overview with current balance

### 📈 Analytics & Visualization
- **Monthly Summary** - Income vs expense comparison
- **Spending Analysis** - Category-wise expenditure breakdown
- **Interactive Charts** - Visual representation of financial data
- **Trend Analysis** - 6-month spending patterns

### 📤 Export Capabilities
- **CSV Export** - Download transactions for spreadsheet analysis
- **PDF Reports** - Professional financial statements
- **Custom Date Ranges** - Flexible export periods (7, 30, 90 days, etc.)
- **Formatted Output** - Clean, readable export formats

### 📱 User Experience
- **Responsive Design** - Mobile-friendly Bootstrap interface
- **Intuitive Navigation** - Easy-to-use dashboard and menus
- **Real-time Validation** - Form validation and error handling
- **Pagination** - Efficient handling of large transaction lists

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User authentication management
- **Werkzeug** - Password hashing and security

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Jinja2** - Templating engine
- **JavaScript** - Client-side interactivity
- **CSS3** - Custom styling and animations

### Data Processing
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization and charting
- **Seaborn** - Enhanced statistical graphics
- **ReportLab** - PDF generation and reporting

### Database
- **SQLite** - Lightweight database (production-ready for PostgreSQL/MySQL)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kirankumarvel/fintrack.git
   cd fintrack
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python init_database.py
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open your browser and navigate to: `http://localhost:5000`

## 🗄️ Database Schema

### Models
- **Users** - User authentication and profile information
- **Transactions** - Income and expense records
- **Categories** - Transaction categorization system

### Relationships
- One-to-Many: User → Transactions
- One-to-Many: User → Categories
- Many-to-One: Transaction → Category

## 🎯 Usage Guide

### Getting Started
1. **Register** a new account or login with existing credentials
2. **Add Transactions** using the "Add Transaction" page
3. **Categorize** each transaction for better organization
4. **View Dashboard** for financial overview and insights

### Managing Finances
- **Add Income**: Salary, freelance work, investments, gifts
- **Track Expenses**: Daily spending, bills, subscriptions, entertainment
- **Review Analytics**: Monthly trends and category spending
- **Generate Reports**: Export data for external analysis

### Advanced Features
- **Edit/Delete**: Modify existing transactions as needed
- **Filter Views**: Pagination for large transaction lists
- **Date Range Selection**: Custom period analysis
- **Chart Updates**: Automatic visualization refreshes

## 🔧 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User authentication
- `GET /logout` - Session termination

### Transactions
- `GET /transactions` - List transactions (paginated)
- `POST /add_transaction` - Create new transaction
- `POST /edit_transaction/<id>` - Update transaction
- `GET /delete_transaction/<id>` - Remove transaction

### Analytics
- `GET /dashboard` - Financial overview
- `GET /analytics` - Spending analysis and charts
- `GET /api/chart_data` - JSON data for visualizations

### Export
- `GET /export` - Export options page
- `GET /export_csv` - Download CSV report
- `GET /export_pdf` - Download PDF report

## 🚀 Deployment

### Production Deployment
1. **Set Environment Variables**
   ```bash
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   ```

2. **Use Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure Web Server** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 🧪 Testing

### Run Tests
```bash
python -m pytest tests/ -v
```

### Test Coverage
```bash
coverage run -m pytest
coverage report
coverage html
```

## 📁 Project Structure

```
FinTrack/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Dependencies
├── init_database.py      # Database initialization
├── tests/               # Test cases
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── dashboard.html   # Dashboard
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── transactions.html # Transactions list
│   ├── add_transaction.html # Add transaction
│   ├── edit_transaction.html # Edit transaction
│   ├── analytics.html   # Analytics page
│   └── export.html      # Export page
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Custom styles
│   ├── js/
│   │   └── script.js    # JavaScript functions
│   └── charts/          # Generated charts
└── utils/               # Utility functions
    ├── analytics.py     # Data analysis functions
    └── export.py        # Export functionality
```

## 🔒 Security Features

- Password hashing with Werkzeug
- SQL injection prevention through ORM
- XSS protection with template auto-escaping
- CSRF protection via session management
- User-specific data isolation
- Input validation and sanitization

## 📈 Performance Optimizations

- Database indexing for faster queries
- Pagination for large datasets
- Chart caching to reduce processing
- Efficient SQL queries with joins
- Static file compression

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation accordingly
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap team for responsive UI components
- Pandas and Matplotlib for data analysis capabilities
- ReportLab for PDF generation features

## 📞 Support

For support, please open an issue on GitHub or contact:
- Website: [https://kirankumarvel.wordpress.com/](https://kirankumarvel.wordpress.com/)
- GitHub: [@Kirankumarvel](https://github.com/Kirankumarvel/)

## 🚦 Roadmap

### Upcoming Features
- [ ] Budget planning and alerts
- [ ] Recurring transactions
- [ ] Investment tracking
- [ ] Multi-currency support
- [ ] Data import from banks
- [ ] Mobile application
- [ ] Advanced reporting
- [ ] API for third-party integrations

### Technical Improvements
- [ ] PostgreSQL migration
- [ ] Async processing
- [ ] Advanced caching
- [ ] Unit test coverage
- [ ] Performance benchmarking

---

**FinTrack** - Take control of your finances with powerful tracking and analytics tools built on Python Flask.
