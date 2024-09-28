from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Check if data is None or empty
        if data is None:
            return json.dumps({'message': 'No data found'})

        response = {}
        if 'ErrorDetail' in str(data):
            response['errors'] = data  # Assuming data has ErrorDetail
        else:
            response = data  # Directly assign data

        return json.dumps(response)
