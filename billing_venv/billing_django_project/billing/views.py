from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .forms import UserRegisterForm, UserFeedback, CartItemForm
from .models import Feedback, Cart, CartItem, Invoice, InvoiceItem
from product_grocery.models import Product, Category


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
        context = super().get_context_data(**kwargs)
        context['total_categories'] = Category.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_admins'] = User.objects.filter(is_staff=True).count()
        context['total_users'] = User.objects.filter(is_staff=False, is_active=True).count()
        context['user_requests'] = User.objects.filter(is_active=False, is_staff=False).count()
        context['raised_issues'] = Feedback.objects.count()
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
# billing/views.py
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('view_cart')
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
        invoice = Invoice.objects.create(user=request.user, total_amount=0)
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

