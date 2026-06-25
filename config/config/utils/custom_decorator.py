from django.contrib.auth.decorators import login_required, user_passes_test

def staff_or_superuser_required(view):
    return user_passes_test(
        lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
        login_url="login",
    )(view)