from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import SteamAccount

@require_GET
def login_page(request, pk):
    acc = get_object_or_404(SteamAccount, pk=pk)
    try:
        code, left = acc.get_steam_code()
    except Exception:
        code, left = "Ошибка", 0
    return render(request, "core/login_page.html", {
        "account": acc, "code": code, "seconds_left": left
    })

@require_GET
def login_json(request, pk):
    """Возвращает код в формате JSON по id"""
    acc = get_object_or_404(SteamAccount, pk=pk)
    try:
        code, left = acc.get_steam_code()
        return JsonResponse({
            "login": acc.login,
            "code": code,
            "seconds_left": left
        })
    except Exception as e:
        print("🔥 Ошибка генерации:", repr(e))
        import traceback; traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

@require_GET
def login_page_by_login(request, login):
    acc = get_object_or_404(SteamAccount, login__iexact=login)
    try:
        code, left = acc.get_steam_code()
    except Exception:
        code, left = "Ошибка", 0
    return render(request, "core/login_page.html", {
        "account": acc, "code": code, "seconds_left": left
    })

@require_GET
def login_json_by_login(request, login):
    acc = get_object_or_404(SteamAccount, login__iexact=login)
    try:
        code, left = acc.get_steam_code()
        return JsonResponse({
            "login": acc.login,
            "code": code,
            "seconds_left": left
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
