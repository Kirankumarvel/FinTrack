import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from models import Transaction, Category
from datetime import datetime, timedelta
import os

def generate_analytics_data(user_id):
    # Get transactions from the last 6 months
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= six_months_ago
    ).all()
    
    if not transactions:
        return {}
    
    # Create DataFrame for easier analysis
    data = []
    for t in transactions:
        data.append({
            'date': t.date,
            'amount': t.amount,
            'type': t.type,
            'category': t.category_rel.name
        })
    
    df = pd.DataFrame(data)
    
    # Monthly spending
    df['month'] = df['date'].dt.to_period('M')
    monthly_spending = df[df['type'] == 'expense'].groupby('month')['amount'].sum().to_dict()
    
    # Category spending
    category_spending = df[df['type'] == 'expense'].groupby('category')['amount'].sum().sort_values(ascending=False).to_dict()
    
    # Monthly income
    monthly_income = df[df['type'] == 'income'].groupby('month')['amount'].sum().to_dict()
    
    # Convert period objects to strings for JSON serialization
    monthly_spending = {str(k): v for k, v in monthly_spending.items()}
    monthly_income = {str(k): v for k, v in monthly_income.items()}
    
    return {
        'monthly_spending': monthly_spending,
        'category_spending': category_spending,
        'monthly_income': monthly_income,
        'total_transactions': len(transactions)
    }

def create_spending_chart(user_id):
    # Get category spending data
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= six_months_ago,
        Transaction.type == 'expense'
    ).join(Category).all()
    
    if not transactions:
        return None
    
    # Prepare data for chart
    category_totals = {}
    for t in transactions:
        category_name = t.category_rel.name
        category_totals[category_name] = category_totals.get(category_name, 0) + t.amount
    
    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%')
    plt.title('Spending by Category')
    
    # Save chart
    chart_dir = os.path.join('static', 'charts')
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)
    
    chart_path = os.path.join(chart_dir, f'chart_{user_id}.png')
    plt.savefig(chart_path)
    plt.close()
    
    return chart_path