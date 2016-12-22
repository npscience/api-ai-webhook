#!/usr/bin/env python

import os

from flask import Flask

# Flask app should start in global layout
app = Flask(__name__)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
