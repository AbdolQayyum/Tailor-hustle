from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import reverse_lazy

from authentication.views import (
    SignInView,
    SignUpView, 
    SignOutView,
    PRView, PRDoneView, PRConfirmView, PRCompleteView,
    PChangeView, PChangeDoneView,
    )

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin_url'),
    path('signup/', SignUpView.as_view(), name='signup_url'),
    path('signout/', SignOutView.as_view(), name='signout_url'),
    
    path('password/reset/', PasswordResetView.as_view(
            email_template_name = 'authentication/password_reset_email.html',
            template_name = 'authentication/password_reset.html'), 
            name='password_reset'),
    
    path('password/reset/done/', PasswordResetDoneView.as_view(
            template_name = 'authentication/password_reset_done.html'),
            name='password_reset_done'),

    path('password/reset/confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
            template_name = 'authentication/password_reset_confirm.html'), 
            name='password_reset_confirm'),

    path('password/reset/complete/', PasswordResetCompleteView.as_view(
            template_name = 'authentication/password_reset_complete.html'), 
            name='password_reset_complete'),

# Rset and change are same so moving forword with reset as of now 

#     path('password/change/', PasswordChangeView.as_view(
#             template_name = 'authentication/password_change.html',
#             success_url = reverse_lazy('password_change_done_view')), 
#             name='password_reset'),

    path('password/change/done/', PasswordResetDoneView.as_view(
            template_name = 'authentication/password_change_done.html'), 
            name='password_change_done_view')
]