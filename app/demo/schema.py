import graphene
from django.contrib.auth.models import User
from graphene_django import DjangoObjectType

from .models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = ("id", "title", "body")


class InternalUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_superuser", "last_login")


class Query(graphene.ObjectType):
    notes = graphene.List(NoteType)
    internal_users = graphene.List(InternalUserType)
    internal_ledger_balance = graphene.Int(account=graphene.String())

    def resolve_notes(root, info):
        return Note.objects.all()

    def resolve_internal_users(root, info):
        return User.objects.all()

    def resolve_internal_ledger_balance(root, info, account=None):
        return 1337


class RotateApiKey(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    key = graphene.String()

    def mutate(root, info, user_id):
        return RotateApiKey(key="rotated")


class Mutation(graphene.ObjectType):
    rotate_api_key = RotateApiKey.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
