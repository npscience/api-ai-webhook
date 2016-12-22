#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import make_response
from flask import request

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

    return {
        'speech': 'Articles about ' + req.get('result').get('parameters').get('subject'),
        'displayText': 'Articles about ' + req.get('result').get('parameters').get('subject')
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
