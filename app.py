#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import make_response
from flask import request
from urllib2 import Request, urlopen

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print('Request:')
    print(json.dumps(req, indent=4))

    r = make_response(json.dumps(processRequest(req), indent=4))

    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get('result').get('action') != "articles.list":
        return {}

    subject = req.get('result').get('parameters').get('subject')

    api_gateway_uri = 'https://prod--gateway.elifesciences.org'

    q = Request(api_gateway_uri + '/subjects/' + subject)
    q.add_header('Accept', 'application/vnd.elife.subject+json;version=1')

    print api_gateway_uri + '/subjects/' + subject
    print(q.headers)

    subject = urlopen(q)

    if subject.getcode() != 200:
        return {}

    subject = json.loads(subject.read())

    return {
        'speech': 'Articles about ' + subject.get('name'),
        'displayText': 'Articles about ' + subject.get('name')
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
