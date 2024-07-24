import io
import stripe
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView
from .forms import UserRegisterForm, UserFeedback, CartItemForm, PaymentForm
from .models import Feedback, Cart, CartItem, Invoice, InvoiceItem
from product_grocery.models import Product, Category
from xhtml2pdf import pisa
from email.mime.application import MIMEApplication
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse


def home(request):
    data_context = {
        'title': 'Home Page - QUICK CART HUB',
    }
    return render(request, 'home.html', data_context)


def about(request):
    return render(request, template_name='about.html', context={'title': 'About Page - QUICK CART HUB'})


@staff_member_required
def userlist(request):
    users = User.objects.all()
    context = {
        'users': users,
        'title': 'users of QUICK CART HUB'
    }
    return render(request, template_name='admin/manage_user.html', context=context)


class AdminLogin(LoginView):
    template_name = 'admin/admin_login.html'
    success_url = reverse_lazy('dashboard_admin')

    def get_success_url(self):
        return self.success_url


class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard_admin.html'

    def get_context_data(self, **kwargs):
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year

        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_users'] = User.objects.count()
        context['total_act_users'] = User.objects.filter(is_active=True).count()
        context['total_admins'] = User.objects.filter(is_staff=True).count()
        context['total_biller'] = User.objects.filter(is_staff=False, is_active=True).count()
        context['user_requests'] = User.objects.filter(is_active=False, is_staff=False).count()
        context['raised_issues'] = Feedback.objects.count()
        context['review_feedback'] = Feedback.objects.filter(reviewed=False).count()
        context['raised_issues'] = Feedback.objects.count()
        context['invoice_count'] = Invoice.objects.count()
        context['invoice_count_today'] = Invoice.objects.filter(created_at__date=today).count()
        context['invoice_count_this_month'] = Invoice.objects.filter(created_at__year=current_year,
                                                                     created_at__month=current_month).count()
        context['invoice_count_this_year'] = Invoice.objects.filter(created_at__year=current_year).count()

        return context


class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    if User.is_superuser:
        success_url = reverse_lazy('dashboard_admin')
    else:
        success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('bill_user_home')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_superuser:
            messages.error(self.request, 'Not an user.')
            return redirect('home_page')
        else:
            if user.is_active:
                login(self.request, user)
                return redirect(self.success_url)
            else:
                messages.error(self.request, 'Your account is not approved yet.')
                return redirect('login_user')


class UserDashHome(TemplateView):
    template_name = 'billing/billing_home.html'


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_next_page(self):
        if self.request.user.is_staff:
            return 'home_page'
        else:
            return 'home_page'


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/change_pass.html'
    success_url = reverse_lazy('bill_user_home')

    def form_valid(self, form):
        messages.success(self.request, "Password Changed")
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'old_password' in form.errors:
            messages.error(self.request, "Invalid Password")
        elif 'new_password2' in form.errors:
            messages.error(self.request, "Password not matching")
        return super().form_invalid(form)


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@admin_required
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('dashboard_admin')  # Adjust this to your admin page URL name


@admin_required
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    delete_user(request, user_id)
    return redirect('dashboard_admin')


@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('dashboard_admin')


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = UserFeedback(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_thanks')
    else:
        form = UserFeedback()
    return render(request, 'users/submit_feedback.html', {'form': form})


@login_required
def feedback_thanks(request):
    return render(request, 'users/feedback_thanks.html')


@admin_required
def manage_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin/manage_feedback.html', {'feedback_list': feedback_list})


@admin_required
def review_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.reviewed = True
    feedback.save()
    return redirect('manage_feedback')


@admin_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('dashboard_admin')  # Adjust this to your admin page URL name


# cart views
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('generate_invoice')
    else:
        form = CartItemForm()
    return render(request, 'billing/add_to_cart.html', {'form': form})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('prepare_bill')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'billing/view_cart.html', {'cart_items': cart_items})


@login_required
def generate_invoice(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if cart_items.exists():

        customer_name = request.POST.get('customer_name')
        customer_mobile = request.POST.get('customer_mobile')
        customer_email = request.POST.get('customer_email')
        invoice = Invoice.objects.create(user=request.user, total_amount=0, customer_email=customer_email,
                                         customer_name=customer_name,
                                         customer_mobile=customer_mobile)
        total_amount = 0

        for item in cart_items:
            invoice_item = InvoiceItem.objects.create(
                invoice=invoice,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price * item.quantity
            )
            total_amount += invoice_item.price

        invoice.total_amount = total_amount
        invoice.save()
        cart_items.delete()
        return render(request, 'billing/invoice.html',
                      {'invoice': invoice, 'invoice_items': invoice.invoiceitem_set.all()})
    else:
        return redirect('view_cart')


@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice})


@login_required
def prepare_bill(request):
    query = request.GET.get('n', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('prepare_bill')
    else:
        form = CartItemForm()
    return render(request, 'billing/cart.html', {
        'products': products,
        'cart_items': cart_items,
        'form': form,
    })


@login_required
def send_invoice_email(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    customer_email = invoice.customer_email
    subject = 'Invoice from QUICK CART HUB'
    message = f'Thank you for your purchase.\nYour total billing amount is {invoice.total_amount}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [customer_email]

    pdf = render_to_pdf('billing/invoice.html',
                        {'invoice': invoice, 'invoice_items': invoice.invoiceitem_set.all()})

    if pdf:
        email = EmailMessage(subject, message, email_from, recipient_list)
        pdf_attachment = MIMEApplication(pdf, _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"invoice_{invoice.id}.pdf")
        email.attach(pdf_attachment)

        try:
            email.send()
            return redirect('prepare_bill')
        except Exception as e:
            # content1 = {
            #     'status': 'error',
            #     'message': str(e)
            # }
            # return render('prepare_bill', content1)
            return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to generate PDF'})

        # send_mail(subject, message, email_from, recipient_list)
    return render(request, 'billing/invoice.html',
                  {'invoice': invoice, 'invoice_items': invoice.invoiceitem_set.all(), 'email_sent': True})


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None


# payment methods
# Kg@#stripes12345

stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = int(form.cleaned_data['amount'] * 100)  # Stripe uses cents
            try:
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    description='Payment',
                    source=request.POST['stripeToken']
                )
                # Save payment information to the database
                # Payment.objects.create(user=request.user, amount=form.cleaned_data['amount'], status='Paid')
                return redirect('payment_success')
            except stripe.error.StripeError:
                return redirect('payment_error')
    else:
        form = PaymentForm()
    return render(request, 'billing/payment.html',
                  {'form': form, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})
