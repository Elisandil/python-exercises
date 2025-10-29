from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from typing import List, Dict, Any
from datetime import datetime


def generate_pdf_report(tasks: List[Dict[str, Any]], file_name: str = "task_report.pdf") -> None:
    """
    Genera un reporte PDF con todas las tareas
    
    Args:
        tasks: Lista de tareas en formato diccionario
        file_name: Nombre del archivo PDF a generar
    """
    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1  # Centro
    )
    
    title = Paragraph("Reporte de Tareas", title_style)
    elements.append(title)
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=1
    )
    date_text = Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", date_style)
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    completed = sum(1 for task in tasks if task['completada'])
    total = len(tasks)
    summary_text = f"Total de tareas: {total} | Completadas: {completed} | Pendientes: {total - completed}"
    summary = Paragraph(summary_text, styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 0.3*inch))
    
    if tasks:
        data = [['ID', 'Nombre', 'Prioridad', 'Estado', 'Categoría']]
        
        for task in tasks:
            estado = '✓ Completada' if task['completada'] else '○ Pendiente'
            categoria = task['categoria'].get('primaria', 'Sin categoría')
            prioridad_map = {1: 'Alta', 2: 'Media', 3: 'Baja'}
            prioridad = prioridad_map.get(task['prioridad'], str(task['prioridad']))
            
            data.append([
                str(task['id']),
                task['nombre'][:30] + '...' if len(task['nombre']) > 30 else task['nombre'],
                prioridad,
                estado,
                categoria
            ])
        
        table = Table(data, colWidths=[0.5*inch, 3*inch, 1*inch, 1.3*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),  
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
    else:
        no_tasks = Paragraph("No hay tareas para mostrar.", styles['Normal'])
        elements.append(no_tasks)

    doc.build(elements)