from .models import SiteVisit

class SiteVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request - Log visit
        if not request.path.startswith('/admin/') and not request.path.startswith('/media/') and not request.path.startswith('/static/'):
            try:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                
                SiteVisit.objects.create(
                    path=request.path,
                    ip_address=ip,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except Exception:
                pass  # Don't crash on logging failure

        response = self.get_response(request)
        return response
