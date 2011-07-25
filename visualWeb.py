#!/usr/bin/env python
from flask import Flask, jsonify, render_template, request
import sys
import lxml
from lxml import html, etree
import urllib
import os
import random
import threading

app = Flask(__name__)
getBeer = 0
dictInputs = {}
@app.route('/')
def index():
    return 'Index Page'

@app.route('/beer/')
@app.route('/beer/<beer>')
def beer(beer=None):
    return render_template('beer.html', beer=beer)

@app.route('/api', methods=['POST','GET'])
def api():
    global dictInputs
    for args in request.args:
        dictInputs[args] = request.args[args]
    print >>sys.stderr,dictInputs
    return ""

@app.route('/_updateLegi')
def updateLegi():
    global dictInputs
    print >>sys.stderr,jsonify(dictInputs)
    return jsonify(dictInputs)
    
    
@app.route('/_updateContent')
def updateContent():
    file = urllib.urlopen('https://www.amiv.ethz.ch')
    root = html.parse(file).getroot()
    content = root.get_element_by_id('content')
    contentString = etree.tostring(content)
    return jsonify(result = contentString)
    
@app.route('/_getImg')
def updateImg():
    path = 'static/gallery/'
    listing = os.listdir(path)
    randomImg = random.randint(0,len(listing)-1)
    print >>sys.stderr, path + listing[randomImg]
    return jsonify(result = path + listing[randomImg])

def simulateStep(getParams):
    """Simulates a certain action normaly sent by core
    :param getParams: dict which should be used like it was sent from core.py"""
    global dictInputs
    for args in getParams:
        dictInputs[args] = getParams[args]
    
@app.route('/simulate')
def simulate():
    """Will cause a sequential change of the dictInputs-state-array to mimic someone getting a beer, someone not registered and someone not authorized"""
    threading.Timer(3,simulateStep,args=[{'page': 'authorized','sponsor': 'AMIV'}]).start()
    threading.Timer(6,simulateStep,args=[{'page': 'freeBeer','sponsor': 'AMIV'}]).start()
    threading.Timer(9,simulateStep,args=[{'page': 'notAuthorized','sponsor': 'AMIV'}]).start()
    threading.Timer(12,simulateStep,args=[{'page': 'notRegistered','sponsor': 'AMIV'}]).start()
    threading.Timer(15,simulateStep,args=[{'page': ''}]).start()
    return "Started simulation"

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)
