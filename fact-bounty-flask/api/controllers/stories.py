from flask.views import MethodView
from flask import make_response, request, jsonify, current_app
from elasticsearch.helpers import scan

class AllStories(MethodView):
    """
    Retrieve stories

    :return: JSON object with all stories and HTTP status code 200.
    """
    def get(self):
        doc = {'query': {'match_all': {}}}
        stories = {}
        try:
            for story in scan(current_app.elasticsearch, doc, index='factbounty', doc_type='story'):
                PID = story['_id']
                source = story['_source']
                stories[PID] = source
        except Exception as e:
            # An error occured, therefore return a string message containing the error
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

        response = {
            'message': 'Stories successfully fetched',
            'stories': stories
        } 
        return make_response(jsonify(response)), 200


class GetRange(MethodView):
    """
    Retrieve stories in range
    
    :return: JSON object with range of stories and HTTP status code 200.
    """
    def get(self, page):
        stories = []
        try:
            search = current_app.elasticsearch.search(
                index='factbounty', doc_type='story', body={
                    'query': {'match_all': {}},
                    'from': (page - 1) * current_app.config['POSTS_PER_PAGE'], 'size': current_app.config['POSTS_PER_PAGE']
                }
            )
            for story in search['hits']['hits']:
                PID = story['_id']
                source = story['_source']
                source['_id'] = PID
                stories.append(source)
        except Exception as e:
            # An error occured, therefore return a string message containing the error
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

        response = {
            'message': 'Stories successfully fetched',
            'stories': stories
        } 
        return make_response(jsonify(response)), 200


class ChangeUpvote(MethodView):
    """
    Update upvote-count
    
    :param request: the request being processed
    """
    def post(self):
        try:
            # extract data from request
            data = request.get_json(silent=True)
            _id = data['story_id']
            value = data['change_val']

            # get earlier count of that story
            count = current_app.elasticsearch.get(index='factbounty', doc_type='story', id=_id)['_source']['approved_count']
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404

        # now update the story vote
        try:
            current_app.elasticsearch.update(index='factbounty', doc_type='story', id=_id, body={"doc": {"approved_count": (count + value)}})
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

        response = {
            'message': 'Changed upvote successfully'
        } 
        return make_response(jsonify(response)), 200


class ChangeDownvote(MethodView):
    """
    Update fake-count
    
    :param request: the request being processed
    """
    def post(self):
        
        try:
            # extract data from request
            data = request.get_json(silent=True)
            _id = data['story_id']
            value = data['change_val']

            # get earlier count of that story
            count = current_app.elasticsearch.get(index='factbounty', doc_type='story', id=_id)['_source']['fake_count']
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404

        # now update the story vote
        try:
            current_app.elasticsearch.update(index='factbounty', doc_type='story', id=_id, body={"doc": {"fake_count": (count + value)}})
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

        response = {
            'message': 'Changed downvote successfully'
        } 
        return make_response(jsonify(response)), 200


class ChangeMixvote(MethodView):
    """
    Update mixedvote-count
    
    :param request: the request being processed
    """
    def post(self):

        try:
            # extract data from request
            data = request.get_json(silent=True)
            _id = data['story_id']
            value = data['change_val']

            # get earlier count of that story
            count = current_app.elasticsearch.get(index='factbounty', doc_type='story', id=_id)['_source']['mixedvote_count']
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 404

        # now update the story vote
        try:
            current_app.elasticsearch.update(index='factbounty', doc_type='story', id=_id, body={"doc": {"mixedvote_count": (count + value)}})
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

        response = {
            'message': 'Changed mixedvote successfully'
        } 
        return make_response(jsonify(response)), 200


storyController = {
    'allstories': AllStories.as_view('all_stories'),
    'getrange': GetRange.as_view('get_range'),
    'changedownvote': ChangeDownvote.as_view('change_downvote'),
    'changemixvote': ChangeMixvote.as_view('change_mixvote'),
    'changeupvote': ChangeUpvote.as_view('change_upvote')
}