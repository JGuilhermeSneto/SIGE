from django.urls import path
from ..views.honeypot import honeypot_trap

urlpatterns = [
    path("wp-admin/", honeypot_trap),
    path("wp-login.php", honeypot_trap),
    path(".env", honeypot_trap),
    path("xmlrpc.php", honeypot_trap),
    path("phpmyadmin/", honeypot_trap),
    path("config.php", honeypot_trap),
    path(".git/", honeypot_trap),
]
