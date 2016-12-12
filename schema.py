# -*- coding: utf-8 -*-
import random
import graphene


# Enums

class Gender(graphene.Enum):
    MALE = 'male'
    FEMALE = 'female'


# Queries

class Character(graphene.Interface):
    id = graphene.ID()
    name = graphene.String()


class Human(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    gender = graphene.Field(Gender)


class HumanQuery(graphene.AbstractType):
    humans = graphene.List(Human)
    human = graphene.Field(Human, id=graphene.Int())

    def resolve_humans(self, args, context, info):
        return humans

    def resolve_human(self, args, context, info):
        for h in humans:
            if h.id == args.get('id'):
                return h


humans = [
    Human(
        id=i,
        name='human {0}'.format(i),
        gender=random.choice([Gender.MALE.value, Gender.FEMALE.value])
    )
    for i in range(1, 11)
]


class Query(HumanQuery, graphene.ObjectType):
    pass


# Mutations

class CreateHuman(graphene.Mutation):
    class Input:
        name = graphene.String(required=True)
        gender = graphene.Argument(Gender, required=True)

    ok = graphene.Boolean()
    human = graphene.Field(lambda: Human)

    def mutate(self, args, context, info):
        human = Human(
            id=humans[-1].id + 1,
            name=args.get('name'),
            gender=args.get('gender'),
            )
        humans.append(human)
        return CreateHuman(human=human, ok=True)


class HumanMutation(graphene.AbstractType):
    create_human = CreateHuman.Field()


class Mutation(HumanMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
