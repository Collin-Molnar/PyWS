#!flask/bin/python

'''
Created on Apr 11, 2015

@author: molnar
'''
from flask import Flask, request
from __main__ import StringIO
from gps.ProcessPos import ProcessPos

app = Flask(__name__)
ouput = StringIO.StringIO()

@app.route('/gps/data/position/<station>/v2')
def gps(station):
    referenceFrame = request.args.get('referenceFrame')          #    nam08
    analysisCenter = request.args.get('analysis_center')          #    pbo&
    starttime = request.args.get('starttime')                    #    2006-01-01T00%3A00%3A00&
    endtime = request.args.get('endtime')                        #    2012-03-01T00%3A00%3A00&
    tsFormat = request.args.get('tsFormat')                      #    iso8601&
    stdDevRange = request.args.get('std_dev_range')                #    false
    
    create_output()
    
    ARCHIVE_POS_LOCS = "pub/products/position"
    file_location = ARCHIVE_POS_LOCS + '/' + station + '/' + station + "analysis_center" + referenceFrame + ".pos"
    pp = ProcessPos(file_location)
    result = pp.getoutput()
    
def create_output():
    

@app.route('/')
def init():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
