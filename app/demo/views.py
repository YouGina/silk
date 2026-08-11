from django.http import JsonResponse

from .models import Note


def index(request):
    # A normal app view that touches the DB, so profilers have something to record.
    return JsonResponse({"notes": list(Note.objects.values("id", "title"))})


def secretish(request):
    # Simulates a real authenticated API call whose request/response a profiler
    # would capture: bearer token in the header, PII in the body.
    Note.objects.filter(title="victim-private-record").count()
    return JsonResponse({"ssn": "123-45-6789", "email": "victim@example.com"})
