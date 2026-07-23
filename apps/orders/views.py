# Orders views — list, detail, cancel, PDF download
import io
import uuid
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from apps.orders.models import Order


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-placed_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_tracking(request, order_id):
    """Customer's live order tracking view."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    tracking = getattr(order, 'tracking', None)
    return render(request, 'orders/tracking.html', {
        'order': order,
        'tracking': tracking
    })


@login_required
def order_cancel(request, order_id):
    """Allow user to cancel their own order (only if placed/confirmed)."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        if order.status not in ('placed', 'confirmed'):
            messages.error(request, 'This order cannot be cancelled at this stage.')
            return redirect('orders:detail', order_id=order_id)

        reason = request.POST.get('reason', '').strip() or 'Cancelled by customer'
        order.status = 'cancelled'
        order.cancel_reason = reason
        order.cancelled_at = timezone.now()
        order.save()
        messages.success(request, f'Order {order.order_number} has been cancelled.')
        return redirect('orders:list')

    return redirect('orders:detail', order_id=order_id)


@login_required
def order_pdf(request, order_id):
    """Generate and download a PDF invoice for the order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Unique PDF serial number for security
    pdf_serial = f'SKS-INV-{order.order_number}-{order.id:05d}'

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import cm
        from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                         Paragraph, Spacer, HRFlowable)
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
        from django.conf import settings as django_settings

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=1.5*cm, leftMargin=1.5*cm,
                                topMargin=1.5*cm, bottomMargin=1.5*cm)

        styles = getSampleStyleSheet()
        story  = []

        # ─── Color palette ───
        GREEN_DARK  = colors.HexColor('#1a5d1a')
        GREEN_LIGHT = colors.HexColor('#e8f5e9')
        GREY_DARK   = colors.HexColor('#222222')
        GREY_LIGHT  = colors.HexColor('#f8faf8')
        GREY_TEXT   = colors.HexColor('#666666')
        BORDER_CLR  = colors.HexColor('#dce8dc')

        # ─── ReportLab Paragraph Styles (Strict Leading to Prevent Overlap) ───
        title_style = ParagraphStyle(
            'HeaderTitle', parent=styles['Normal'],
            fontSize=22, leading=26, fontName='Helvetica-Bold',
            textColor=GREEN_DARK, alignment=TA_CENTER, spaceAfter=4
        )
        sub_style = ParagraphStyle(
            'HeaderSub', parent=styles['Normal'],
            fontSize=9, leading=13, fontName='Helvetica',
            textColor=GREY_TEXT, alignment=TA_CENTER, spaceAfter=8
        )
        inv_title_style = ParagraphStyle(
            'InvTitle', parent=styles['Normal'],
            fontSize=13, leading=17, fontName='Helvetica-Bold',
            textColor=GREEN_DARK, alignment=TA_CENTER, spaceAfter=2
        )
        serial_style = ParagraphStyle(
            'SerialStyle', parent=styles['Normal'],
            fontSize=8, leading=11, fontName='Helvetica',
            textColor=GREY_TEXT, alignment=TA_CENTER, spaceAfter=10
        )
        sec_heading = ParagraphStyle(
            'SecHeading', parent=styles['Normal'],
            fontSize=10, leading=14, fontName='Helvetica-Bold',
            textColor=GREEN_DARK, spaceAfter=6
        )
        label_style = ParagraphStyle(
            'Label', parent=styles['Normal'],
            fontSize=8, leading=11, fontName='Helvetica-Bold',
            textColor=GREY_TEXT
        )
        value_style = ParagraphStyle(
            'Value', parent=styles['Normal'],
            fontSize=9, leading=12, fontName='Helvetica',
            textColor=GREY_DARK
        )
        th_style = ParagraphStyle(
            'TH', parent=styles['Normal'],
            fontSize=9, leading=12, fontName='Helvetica-Bold',
            textColor=colors.white
        )

        # ─── 1. STORE HEADER ───
        store_name = getattr(django_settings, 'STORE_NAME', 'Shivank Kirana Store')
        store_addr = getattr(django_settings, 'STORE_ADDRESS', '288, Main Market, Meerut - 250404')
        store_phone = getattr(django_settings, 'STORE_PHONE', '+917599342112')
        store_email = getattr(django_settings, 'STORE_EMAIL', 'support@shivankkirana.com')

        story.append(Paragraph(store_name, title_style))
        story.append(Paragraph(f'{store_addr} &nbsp;|&nbsp; Phone: {store_phone} &nbsp;|&nbsp; Email: {store_email}', sub_style))
        story.append(Spacer(1, 0.1*cm))
        story.append(HRFlowable(width='100%', thickness=1.5, color=GREEN_DARK, spaceAfter=10))

        # ─── 2. INVOICE TITLE & SERIAL ───
        story.append(Paragraph('TAX INVOICE / ORDER RECEIPT', inv_title_style))
        story.append(Paragraph(f'Invoice Serial No: <b>{pdf_serial}</b>', serial_style))

        # ─── 3. ORDER & CUSTOMER INFORMATION GRID ───
        def info_row(lbl, val):
            return [Paragraph(lbl, label_style), Paragraph(str(val), value_style)]

        placed_str = order.placed_at.strftime('%d %b %Y, %I:%M %p') if order.placed_at else '—'
        delivered_str = order.delivered_at.strftime('%d %b %Y') if order.delivered_at else 'In Progress'

        order_info_data = [
            info_row('Order Number:', order.order_number),
            info_row('Order Date:', placed_str),
            info_row('Payment Method:', order.payment_method),
            info_row('Payment Status:', order.get_payment_status_display()),
            info_row('Order Status:', order.get_status_display()),
            info_row('Delivery Date:', delivered_str),
        ]
        order_table = Table(order_info_data, colWidths=[3.2*cm, 5.2*cm])
        order_table.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, GREY_LIGHT]),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, BORDER_CLR),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        addr = order.address
        addr_str = f'{addr.full_address}, {addr.city}, {addr.pincode}' if addr else 'N/A'
        cust_info_data = [
            info_row('Customer Name:', order.user.full_name),
            info_row('Phone Number:', order.user.phone),
            info_row('Email Address:', order.user.email),
            info_row('Delivery Address:', addr_str),
        ]
        cust_table = Table(cust_info_data, colWidths=[3.2*cm, 5.2*cm])
        cust_table.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, GREY_LIGHT]),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, BORDER_CLR),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        info_wrapper = Table([[order_table, cust_table]], colWidths=['50%', '50%'])
        info_wrapper.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(info_wrapper)
        story.append(Spacer(1, 0.4*cm))

        # ─── 4. ITEMS ORDERED TABLE ───
        story.append(Paragraph('ITEMS ORDERED', sec_heading))

        item_rows = [[
            Paragraph('#', th_style),
            Paragraph('Product Name', th_style),
            Paragraph('Qty', th_style),
            Paragraph('Unit Price', th_style),
            Paragraph('Total Amount', th_style),
        ]]
        for idx, item in enumerate(order.items.all(), 1):
            item_rows.append([
                Paragraph(str(idx), value_style),
                Paragraph(item.product_name, value_style),
                Paragraph(str(item.quantity), value_style),
                Paragraph(f'₹{item.unit_price}', value_style),
                Paragraph(f'₹{item.total_price}', value_style),
            ])

        items_table = Table(item_rows, colWidths=[0.8*cm, 8.5*cm, 1.8*cm, 2.8*cm, 3.1*cm])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), GREEN_DARK),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GREEN_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.3, BORDER_CLR),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.3*cm))

        # ─── 5. SUMMARY & GRAND TOTAL ───
        summary_rows = [
            [Paragraph('Subtotal', label_style), Paragraph(f'₹{order.subtotal}', value_style)],
            [Paragraph('Delivery Charge', label_style), Paragraph(f'₹{order.delivery_charge}', value_style)],
            [Paragraph('Coupon Discount', label_style), Paragraph(f'- ₹{order.coupon_discount}', value_style)],
        ]
        sum_table = Table(summary_rows, colWidths=[13.9*cm, 3.1*cm])
        sum_table.setStyle(TableStyle([
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, GREY_LIGHT]),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.3, BORDER_CLR),
        ]))
        story.append(sum_table)

        grand_text_l = ParagraphStyle('GTL', parent=styles['Normal'], fontSize=11, leading=14, fontName='Helvetica-Bold', textColor=colors.white)
        grand_text_r = ParagraphStyle('GTR', parent=styles['Normal'], fontSize=11, leading=14, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_RIGHT)
        grand_table = Table([[Paragraph('GRAND TOTAL', grand_text_l), Paragraph(f'₹{order.total_amount}', grand_text_r)]], colWidths=[13.9*cm, 3.1*cm])
        grand_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), GREEN_DARK),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(grand_table)
        story.append(Spacer(1, 0.5*cm))

        # ─── 6. FOOTER & VERIFICATION ───
        story.append(HRFlowable(width='100%', thickness=1, color=BORDER_CLR, spaceAfter=8))
        foot_style = ParagraphStyle(
            'FootStyle', parent=styles['Normal'],
            fontSize=7.5, leading=11, fontName='Helvetica',
            textColor=GREY_TEXT, alignment=TA_CENTER
        )
        thanks_style = ParagraphStyle(
            'ThanksStyle', parent=styles['Normal'],
            fontSize=8.5, leading=12, fontName='Helvetica-Bold',
            textColor=GREEN_DARK, alignment=TA_CENTER
        )
        story.append(Paragraph(f'Computer Generated Invoice &nbsp;|&nbsp; Serial: {pdf_serial} &nbsp;|&nbsp; Generated on: {timezone.now().strftime("%d %b %Y %I:%M %p")}', foot_style))
        story.append(Spacer(1, 0.1*cm))
        story.append(Paragraph('Thank you for shopping at Shivank Kirana Store! For support, contact support@shivankkirana.com', thanks_style))

        doc.build(story)
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Invoice_{order.order_number}.pdf"'
        return response

    except ImportError:
        return HttpResponse(
            '<h2>PDF generation requires reportlab.</h2><p>Run: <code>pip install reportlab</code></p>',
            content_type='text/html', status=500
        )
