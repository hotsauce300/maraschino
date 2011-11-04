from flask import Flask, render_template
import json, jsonrpclib, urllib

from htpcfrontend import app
from settings import *
from tools import *

@app.route('/xhr/sabnzbd')
@requires_auth
def xhr_sabnzbd():
    url = '%s&mode=qstatus&output=json' % (SABNZBD_URL)
    result = urllib.urlopen(url).read()
    sabnzbd = json.JSONDecoder().decode(result)

    percentage_total = 0

    if sabnzbd['jobs']:
        percentage_total = int(100 - (sabnzbd['mbleft'] / sabnzbd['mb'] * 100))

    return render_template('sabnzbd.html',
        sabnzbd = sabnzbd,
        percentage_total = percentage_total,
    )