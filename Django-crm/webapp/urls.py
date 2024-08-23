from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/', views.userPage, name="user-page"),
    path('register/', views.signupPage, name='register'),
    path('settings/', views.accountSettings, name='account'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('products/', views.products, name='products'),
    path('create_order/<int:pk>', views.create_order, name='create_order'),
    path('update_order/<int:pk>', views.update_order, name='update'),
    path('delete_order/<int:pk>', views.delete_order, name='delete'),
    path('customer/<int:pk>', views.customers, name='customer'),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name='password_reset_done'),
    path('reset_password_confirm/<uid64>/<token>', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_done.html"),
         name="password_reset_complete"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
