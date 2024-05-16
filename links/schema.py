import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from links.models import Heroe, Vote
from graphql import GraphQLError

class LinkType(DjangoObjectType):
    class Meta:
        model = Heroe

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        return Heroe.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    name = graphene.String()
    description = graphene.String()
    comic = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
        url = graphene.String()
        name = graphene.String()
        description = graphene.String()
        comic = graphene.String()


    #3
    def mutate(self, info, url,name,description,comic):
        user = info.context.user or None

        link = Heroe(
            url=url,
            name=name,
            description=description,
            comic=comic,
            posted_by=user,
            )
        link.save()

        return CreateLink(
            id=link.id,
            name=link.name,
            url=link.url,
            description=link.description,
            comic=link.comic,
            posted_by=link.posted_by,
        )
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            #1
            raise GraphQLError('Debes estar logeado para votar!')

        link = Heroe.objects.filter(id=link_id).first()
        if not link:
            #2
            raise Exception('Link Invalido!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)
#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()