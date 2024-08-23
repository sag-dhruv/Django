from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .filters import OrderFilters
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .decorators import user_is_authenticated, allowed_users, admin_only
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm, CreateUserForm, CustomerForm


@user_is_authenticated
def signupPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
           
            username = form.cleaned_data.get('username')
            messages.info(
                request, 'Account successfully created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


@user_is_authenticated
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(roles=['admin'])
def products(request):
    products = Products.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(roles=['customer'])
def userPage(request):
    '''Only customer user can view page '''
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending, }
    return render(request, 'user.html', context)


@login_required(login_url='login')
@allowed_users(roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'account_settings.html', context)


@login_required(login_url='login')
@allowed_users(roles=['admin'])
def customers(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        orders = customer.order_set.all()
        order_count = orders.count()
        # filter object that takes query params as first param & order object as second
        orderFilter = OrderFilters(request.GET, queryset=orders)
        # show filter orders
        orders = orderFilter.qs
        context = {'customer': customer,
                   'orders': orders, 'order_count': order_count, 'orderFilter': orderFilter}
        return render(request, 'customers.html', context)
    except ObjectDoesNotExist:
        return render(request, 'error.html')


@login_required(login_url='login')
@allowed_users(roles=['admin'])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    # create order formset
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'))
    # create instance of formset
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # # set initial value of customer in order form
    # form = OrderForm(initial={'customer': customer})
    # if we submitting the form then validate & save form data
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    formset = OrderForm(instance=order)
    # submitting the form data of updated id then validate & save form data
    if request.method == 'POST':
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'delete.html', context)
