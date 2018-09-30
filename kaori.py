# coding: UTF-8
import webapp2
from google.appengine.api import taskqueue

class CallbackHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('This Site is API Access Only')

    def post(self):
        params = {
        'signature': self.request.headers['x-line-signature'].rstrip(),
        'body': self.request.body,
        'address': self.request.remote_addr
        }

        taskqueue.add(url='/tasks/receive', target='worker',params=params)
        self.response.write('HTTP 200')

app = webapp2.WSGIApplication([
    ('/callback', CallbackHandler),

], debug=True)
