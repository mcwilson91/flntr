# https://gist.github.com/DmytroLitvinov/39d9a1a93a46eb9da1e17d8e73f35e11
# thanks to DmytroLitvinov for this code

# from django.contrib import messages
# import simplejson
# from .utils import get_messages_dict
#
#
# class AjaxMessaging(object):
#     """
#     Middlware for JSON responses. It adds to each JSON response array with
#     messages from django.contrib.messages framework.
#     It allows handle messages on a page with javascript
#     """
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.
#
#     def __call__(self, request):
#         response = self.get_response(request)
#
#         if request.is_ajax():
#             if response['Content-Type'] in ["static/js"]:
#                 try:
#                     content = simplejson.loads(response.content)
#                     assert isinstance(content, dict)
#                 except (ValueError, AssertionError):
#                     return response
#
#                 content['django_messages'] = [get_message_dict(message) for
#                                               message in
#                                               messages.get_messages(request)]
#
#                 response.content = simplejson.dumps(content)
#         return response
