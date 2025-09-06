from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from models import db, User, Transaction, Category
from config import Config
from utils.analytics import generate_analytics_data, create_spending_chart
from utils.export import export_to_csv, export_to_pdf
from datetime import datetime, timedelta
import os

CSV_MIMETYPE = 'text/csv'
PDF_MIMETYPE = 'application/pdf'

INVALID_DATE_FORMAT_MSG = 'Invalid date format. Please use YYYY-MM-DD.'

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# (Moved basedir definition to init_db())


@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError):
        return None
# Create default categories for new users
def create_default_categories(user):
    expense_categories = ['Food', 'Rent', 'Travel', 'Shopping', 'Utilities', 'Entertainment']
    income_categories = ['Salary', 'Freelance', 'Investment', 'Gift']
    
    for cat in expense_categories:
        category = Category(name=cat, type='expense', user=user)
        db.session.add(category)
    
    for cat in income_categories:
        category = Category(name=cat, type='income', user=user)
        db.session.add(category)
    
    db.session.commit()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        create_default_categories(user)
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= thirty_days_ago
    ).order_by(Transaction.date.desc()).limit(5).all()
    
    # Calculate total income and expenses for the current month
    now = datetime.now()

    month_start = datetime(now.year, now.month, 1)
    
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'income',
        Transaction.date >= month_start
    ).scalar() or 0
    
    total_expenses = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == 'expense',
        Transaction.date >= month_start
    ).scalar() or 0
    
    balance = total_income - total_expenses
    
    # Get analytics data
    analytics_data = generate_analytics_data(current_user.id)
    
    # Generate chart
    chart_path = create_spending_chart(current_user.id)
    
    return render_template('dashboard.html', 
                         transactions=recent_transactions,
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance,
                         analytics=analytics_data,
                         chart_path=chart_path)

@app.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except (ValueError, TypeError):
            flash('Please enter a valid number for the amount.')
            return redirect(url_for('add_transaction'))
        description = request.form['description']
        transaction_type = request.form['type']
        try:
            category_id = int(request.form['category'])
            category_id = int(request.form['category'])
        except (ValueError, TypeError):
            flash('Invalid category selected.')
            return redirect(url_for('add_transaction'))
        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        except (ValueError, TypeError):
            flash(INVALID_DATE_FORMAT_MSG)
            return redirect(url_for('add_transaction'))
            return redirect(url_for('add_transaction'))
        
        category = Category.query.get(category_id)
        if not category or category.user_id != current_user.id:
            flash('Invalid category')
            return redirect(url_for('add_transaction'))
        transaction = Transaction(
            amount=amount,
            description=description,
            type=transaction_type,
            date=date,
            user_id=current_user.id,
            category_id=category_id
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        flash('Transaction added successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html', categories=categories)
    return render_template('add_transaction.html', categories=categories)
@app.route('/transactions')
@login_required
def transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    paginated_transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Transaction.date.desc()
    ).paginate(page=page, per_page=per_page)

    return render_template('transactions.html', transactions=paginated_transactions)
@app.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    
    if transaction.user_id != current_user.id:
        flash('You cannot edit this transaction')
        return redirect(url_for('transactions'))
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        transaction.amount = float(request.form['amount'])
        transaction.description = request.form['description']
        transaction.type = request.form['type']
        transaction.category_id = int(request.form['category'])
        transaction.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        
        db.session.commit()
        flash('Transaction updated successfully!')
        return redirect(url_for('transactions'))
    
    return render_template('edit_transaction.html', 
                         transaction=transaction, 
                         categories=categories)


@app.route('/delete_transaction/<int:id>')
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    
    if transaction.user_id != current_user.id:
        flash('You cannot delete this transaction')
        return redirect(url_for('transactions'))
    
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!')
    return redirect(url_for('transactions'))

@app.route('/analytics')
@login_required
def analytics():
    analytics_data = generate_analytics_data(current_user.id)
    chart_path = create_spending_chart(current_user.id)
    
    return render_template('analytics.html', 
                         analytics=analytics_data,
                         chart_path=chart_path)

@app.route('/export')
@login_required
def export():
    """Main export page that shows export options"""
    return render_template('export.html')

@app.route('/export_csv')
@login_required
def export_csv():
    # Get date range from request or use default (last 30 days)
    days = int(request.args.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)
    
    csv_data = export_to_csv(current_user.id, start_date)
    
    return send_file(
        csv_data,
        as_attachment=True,
        download_name=f'fintrack_export_{datetime.now().strftime("%Y%m%d")}.csv',
        mimetype=CSV_MIMETYPE
    )
# >>> from app import init_db
@app.route('/export_pdf')
@login_required
def export_pdf():
    # Get date range from request or use default (last 30 days)
    days = int(request.args.get('days', 30))
    start_date = datetime.now() - timedelta(days=days)
    pdf_data = export_to_pdf(current_user.id, start_date)
    pdf_data.seek(0)  # Ensure file pointer is at the start
    
    return send_file(
        pdf_data,
        as_attachment=True,
        download_name=f'fintrack_export_{datetime.now().strftime("%Y%m%d")}.pdf',
        mimetype='application/pdf'
    )


with app.app_context():
    db.create_all()
    print("Database created successfully!")
    
    @app.route('/chart_data')
    @login_required
    def chart_data():
        return jsonify(generate_analytics_data(current_user.id))
    
# Context processor to make variables available to all templates
@app.context_processor
def inject_template_vars():
    return {
        'current_year': datetime.now().year,
        'now': datetime.now()
    }

app.run(debug=True, host='0.0.0.0', port=5000)

# API endpoint for chart data
@app.route('/api/chart_data')
@login_required
def chart_data():
    analytics_data = generate_analytics_data(current_user.id)
    return jsonify(analytics_data)