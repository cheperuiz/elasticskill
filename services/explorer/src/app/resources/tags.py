# pylint:disable=import-error
# pylint: disable=no-name-in-module

from flask_restplus import Namespace, Resource, reqparse
from marshmallow import Schema, fields
from elasticsearch.exceptions import TransportError

from database.elasticsearch import es

from tags.search import tags_from_index, aggregate_tags, sort_by_statistics
from utils.common import make_jsend_response

api = Namespace("tags", description="Tags and aggregations.")

fields_by_index = {
    "tasks": ["task", "task_description", "project", "project_description"],
    "threads": ["text"],
}


@api.route("/<string:index>")
@api.param("keywords", "Search matching keywords (comma separated).")
@api.param("operator", "Logic operator when a list of keywords is provided. (defaults to 'or')")
@api.param("skip", "Used for pagination.")
@api.param("limit", "Maximum number of items in response.")
@api.param("fields", "If present, tags will be generated from this fields in each document of the index.")
class Tags(Resource):
    def get(self, index):
        parser = reqparse.RequestParser()
        parser = parser.add_argument("keywords", type=str, default="")
        parser = parser.add_argument("operator", type=str, default="or")
        parser = parser.add_argument("skip", type=int, default=0)
        parser = parser.add_argument("limit", type=int, default=None)
        parser = parser.add_argument("fields", default=fields_by_index.get(index, []))
        params = parser.parse_args()
        print(params["operator"])
        try:
            print(params["keywords"])
            tags = tags_from_index(
                es,
                index=index,
                fields=params["fields"],
                keywords=params["keywords"].split(","),
                operator=params["operator"].lower(),
            )
            aggregated_tags = aggregate_tags(tags)
            sorted_tags = sort_by_statistics(aggregated_tags)

        except TransportError as e:
            return make_jsend_response(code=e.status_code)
        limit = params["skip"] + params["limit"] if params["limit"] else None
        return make_jsend_response(data=sorted_tags[params["skip"] : limit])

