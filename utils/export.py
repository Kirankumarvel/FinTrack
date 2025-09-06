import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from models import Transaction, Category
from datetime import datetime
import io

def export_to_csv(user_id, start_date):
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date
    ).join(Category).order_by(Transaction.date.desc()).all()
    
    data = []
    for t in transactions:
        data.append({
            'Date': t.date.strftime('%Y-%m-%d'),
            'Type': t.type.capitalize(),
            'Category': t.category_rel.name,
            'Amount': t.amount,
            'Description': t.description or ''
        })
    
    df = pd.DataFrame(data)
    
    # Create CSV in memory
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return output

def export_to_pdf(user_id, start_date):
    transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date
    ).join(Category).order_by(Transaction.date.desc()).all()
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph("FinTrack - Transaction Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Summary data
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expenses
    
    summary_data = [
        ["Total Income", f"${total_income:.2f}"],
        ["Total Expenses", f"${total_expenses:.2f}"],
        ["Balance", f"${balance:.2f}"]
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Transaction data
    data = [["Date", "Type", "Category", "Amount", "Description"]]
    
    for t in transactions:
        data.append([
            t.date.strftime('%Y-%m-%d'),
            t.type.capitalize(),
            t.category_rel.name,
            f"${t.amount:.2f}",
            t.description or ''
        ])
    
    table = Table(data, colWidths=[70, 60, 80, 60, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    
    return buffer