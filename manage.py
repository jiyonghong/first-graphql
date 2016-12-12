# -*- coding: utf-8 -*-
from flask import Flask
from flask_graphql import GraphQLView

from schema import schema


app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        )
    )


@app.route('/schema')
def render_schema():
    return str(schema)


if __name__ == '__main__':
    app.debug = True
    app.run()
