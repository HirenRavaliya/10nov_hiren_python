from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def login_view(request):

    if request.user.is_authenticated:
        return redirect("social_auth:dashboard")
    return render(request, "social_auth/login.html")


@login_required(login_url="/q19/login/")
def dashboard(request):

    user = request.user


    social_accounts = []
    try:
        from allauth.socialaccount.models import SocialAccount
        social_accounts = SocialAccount.objects.filter(user=user)
    except Exception:
        pass


    full_name = user.get_full_name() or user.username or user.email.split("@")[0]


    avatar_url = None
    provider_name = "Email"
    for sa in social_accounts:
        if sa.provider == "google":
            avatar_url = sa.extra_data.get("picture")
            provider_name = "Google"
        elif sa.provider == "facebook":
            avatar_url = f"https://graph.facebook.com/{sa.uid}/picture?type=large"
            provider_name = "Facebook"

    context = {
        "user": user,
        "full_name": full_name,
        "avatar_url": avatar_url,
        "provider_name": provider_name,
        "social_accounts": social_accounts,
        "initials": "".join(w[0].upper() for w in full_name.split()[:2]) if full_name else "?",
    }
    return render(request, "social_auth/dashboard.html", context)


def logout_view(request):

    logout(request)
    return redirect("social_auth:login")