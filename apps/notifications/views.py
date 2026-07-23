import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from apps.notifications.models import Notification


@login_required
def notifications_home(request):
    """Customer all-notifications page with 3-day auto-expiry retention logic."""
    now = timezone.now()
    three_days_ago = now - timedelta(days=3)

    # 1. Purge notifications older than 3 days automatically
    Notification.objects.filter(created_at__lt=three_days_ago).delete()

    # 2. Get active notifications for user (created within last 3 days)
    notifications = list(Notification.objects.filter(
        Q(user=request.user) | Q(user__isnull=True),
        created_at__gte=three_days_ago
    ).order_by('-created_at'))

    # 3. Calculate time left and expiration notice for each notification
    for n in notifications:
        expiry_time = n.created_at + timedelta(days=3)
        time_diff = expiry_time - now
        
        hours_left = max(0, int(time_diff.total_seconds() // 3600))
        days_left = hours_left // 24
        rem_hours = hours_left % 24

        if days_left >= 2:
            n.expires_label = f"⏳ Expires in {days_left} days"
            n.expires_class = "exp-safe"
        elif days_left == 1:
            n.expires_label = f"⚠️ Expires in 1 day {rem_hours}h"
            n.expires_class = "exp-warning"
        elif hours_left > 0:
            n.expires_label = f"🔥 Expires in {hours_left} hours"
            n.expires_class = "exp-danger"
        else:
            n.expires_label = "🔥 Expiring soon"
            n.expires_class = "exp-danger"

    # 4. Mark unread as read when user views page
    Notification.objects.filter(
        Q(user=request.user) | Q(user__isnull=True),
        is_read=False
    ).update(is_read=True)

    return render(request, 'notifications/notifications.html', {
        'notifications': notifications,
        'total_count': len(notifications)
    })


@login_required
def notification_detail(request, notif_id):
    """Customer notification detail view."""
    now = timezone.now()
    three_days_ago = now - timedelta(days=3)

    # Fetch notification
    notification = get_object_or_404(
        Notification,
        Q(user=request.user) | Q(user__isnull=True),
        id=notif_id
    )

    # Mark as read
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    # Calculate expiration time remaining
    expiry_time = notification.created_at + timedelta(days=3)
    time_diff = expiry_time - now
    hours_left = max(0, int(time_diff.total_seconds() // 3600))
    days_left = hours_left // 24
    rem_hours = hours_left % 24

    if days_left >= 2:
        expires_label = f"⏳ Expires in {days_left} days"
        expires_class = "exp-safe"
    elif days_left == 1:
        expires_label = f"⚠️ Expires in 1 day {rem_hours}h"
        expires_class = "exp-warning"
    else:
        expires_label = f"🔥 Expires in {hours_left} hours"
        expires_class = "exp-danger"

    # Extract Promo Code if present
    promo_code = None
    if notification.notif_type == 'promo' or 'code' in notification.message.lower() or 'coupon' in notification.message.lower():
        match_code = re.search(r'(?:code|coupon|use|promo)[:\s]+([A-Z0-9]{3,15})', f"{notification.title} {notification.message}", re.IGNORECASE)
        if match_code:
            promo_code = match_code.group(1).upper()
        else:
            matches = re.findall(r'\b[A-Z0-9]{4,15}\b', f"{notification.title} {notification.message}")
            ignore_words = {'FREE', 'OFFER', 'SALE', 'SAVE', 'DISCOUNT', 'SUPER', 'DEAL', 'CODE', 'STORE', 'SPECIAL'}
            for m in matches:
                if m.upper() not in ignore_words and not m.isdigit():
                    promo_code = m.upper()
                    break

    return render(request, 'notifications/detail.html', {
        'n': notification,
        'promo_code': promo_code,
        'expires_label': expires_label,
        'expires_class': expires_class,
        'hours_left': hours_left,
    })


@login_required
def unread_notifications(request):
    """GET /notifications/unread/ — returns unread count + list within 3 days."""
    now = timezone.now()
    three_days_ago = now - timedelta(days=3)
    
    # Auto purge expired notifications older than 3 days
    Notification.objects.filter(created_at__lt=three_days_ago).delete()

    notifs = Notification.objects.filter(
        Q(user=request.user) | Q(user__isnull=True),
        created_at__gte=three_days_ago,
        is_read=False
    ).order_by('-created_at')[:15]

    data = []
    for n in notifs:
        expiry_time = n.created_at + timedelta(days=3)
        time_diff = expiry_time - now
        hours_left = max(0, int(time_diff.total_seconds() // 3600))
        days_left = hours_left // 24

        if days_left >= 2:
            exp_text = f"⏳ {days_left}d left"
        elif days_left == 1:
            exp_text = "⚠️ 1d left"
        else:
            exp_text = f"🔥 {hours_left}h left"

        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.notif_type,
            'action_url': n.action_url or '',
            'created_at': n.created_at.strftime("%d %b, %I:%M %p"),
            'expires_text': exp_text,
        })

    return JsonResponse({'count': len(data), 'notifications': data})


@csrf_exempt
@login_required
def mark_notification_read(request, notif_id):
    """POST /notifications/<id>/read/ — mark a notification as read."""
    if request.method == 'POST':
        Notification.objects.filter(
            Q(id=notif_id),
            Q(user=request.user) | Q(user__isnull=True)
        ).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)
