import graphene
import uvicorn
from fastapi import FastAPI

from graphene import types as grt
from starlette.applications import Starlette
from starlette_graphene import GraphQLApp

import models
from db_conf import db_session
from schemas import PostSchema


db = db_session.session_factory()
#app = FastAPI()
app = Starlette(debug=True)

class CreateNewPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, title, content):
        post = PostSchema(title=title, content=content)
        db_post = models.Post(title=post.title, content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        ok = True
        return CreateNewPost(ok=ok)

class PostMutations(graphene.ObjectType):
    create_new_post = CreateNewPost.Field()

app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(mutation=PostMutations)))
