from api import app, db
from api import models
from api.graphql.query import listPosts_resolver, getPost_resolver
from api.graphql.mutations import create_post_resolver, delete_post_resolver, update_post_resolver
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify

with app.app_context():
    db.create_all()

explorer_html = ExplorerGraphiQL().html(None)


query = ObjectType("Query")
query.set_field("listPosts", listPosts_resolver)
query.set_field("getPost", getPost_resolver)


mutation = ObjectType("Mutation")
mutation.set_field("createPost", create_post_resolver)
mutation.set_field("updatePost", update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
	type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
	data = request.get_json()

	success, result = graphql_sync(
		schema,
		data,
		context_value=request,
		debug=app.debug
	)

	if success:
		status_code = 200
	else:
		status_code = 400

	return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")