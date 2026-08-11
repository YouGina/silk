from django.contrib.auth.models import User
from rest_framework import permissions, serializers, viewsets

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "body"]


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]


class InternalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_staff", "is_superuser", "last_login"]


class InternalUserViewSet(viewsets.ModelViewSet):
    """Staff-only user administration. Should never be reachable anonymously."""

    queryset = User.objects.all()
    serializer_class = InternalUserSerializer
    permission_classes = [permissions.IsAdminUser]


class BillingChargeSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    amount_cents = serializers.IntegerField()
    internal_ledger_account = serializers.CharField()
    override_fraud_check = serializers.BooleanField(default=False)


class InternalBillingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = BillingChargeSerializer

    def create(self, request):
        pass
