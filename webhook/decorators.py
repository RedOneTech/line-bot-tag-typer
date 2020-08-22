from django.http import JsonResponse

from webhook.utils import verify_line_signature

def verify_from_line(func):
    def wrapper(request, *args, **kwargs):
        if verify_line_signature(request):
            return func(request, *args, **kwargs)
        return JsonResponse({
            "detail" : "Failed Verify Authentic Data From LINE"
        }, status=400)
    return wrapper