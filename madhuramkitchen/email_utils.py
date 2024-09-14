from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order, customer_email):
    """
    Send an order confirmation email to the customer.
    """
    # Render the HTML email template for the customer
    subject = 'Order Confirmation'
    message = render_to_string('emails/customer_order.html', {
        'order': order,
        'items': order.items.all(),
        'customer': order.user
    })
    
    # Send the email
    send_mail(
        subject,
        message,  # Plain text fallback (optional, can use empty string)
        settings.DEFAULT_FROM_EMAIL,  # From email
        [customer_email],  # To email
        fail_silently=False,
        html_message=message  # The HTML message
    )

def send_admin_order_notification(order):
    """
    Send an order notification email to the admin with customer and order details.
    """
    admin_email = settings.ADMIN_EMAIL  # Make sure to define this in your settings file

    # Render the HTML email template for the admin
    subject = f'New Order Placed by {order.user.username}'
    message = render_to_string('emails/admin_order_notification.html', {
        'order': order,
        'items': order.items.all(),
        'customer': order.user
    })
    
    # Send the email
    send_mail(
        subject,
        message,  # Plain text fallback (optional, can use empty string)
        settings.DEFAULT_FROM_EMAIL,  # From email
        [admin_email],  # Admin email
        fail_silently=False,
        html_message=message  # The HTML message
    )
