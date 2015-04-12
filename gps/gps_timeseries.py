#!flask/bin/python

'''
Created on Apr 11, 2015

@author: molnar
'''
from flask import Flask, request, send_file
import StringIO
from gps.ProcessPos import ProcessPos
import datetime

app = Flask(__name__)
output = StringIO.StringIO()

@app.route('/gps/data/position/<station>/v2')
def gps(station):
    reference_frame = request.args.get('referenceFrame')          # nam08
    analysis_center = request.args.get('analysisCenter')         # pbo
    starttime = request.args.get('starttime')                    # 2006-01-01T00%3A00%3A00&
    endtime = request.args.get('endtime')                        # 2012-03-01T00%3A00%3A00&
    tsFormat = request.args.get('tsFormat')                      # iso8601&
    stdDevRange = request.args.get('std_dev_range')              # false
    
    ARCHIVE_POS_LOCS = "pub/products/position"
    ISO_8601 = "%Y-%m-%dT%H:%M:%S"
    
    starttime = datetime.datetime.strptime(starttime, ISO_8601)
    endtime = datetime.datetime.strptime(endtime, ISO_8601)
    
    create_output()
    
    print station
    print analysis_center
    print reference_frame
    
    file_location = ARCHIVE_POS_LOCS + "/" + station + "/" + station + "." + analysis_center + "." + reference_frame + ".pos"
    pp = ProcessPos(file_location)
    result = pp.getoutput().splitlines()
    print starttime
    print endtime

    
    for line in result:
        tempdate = line.split()[0]
        tempdate = datetime.date(int(tempdate[:4]), int(tempdate[4:6]), int(tempdate[6:]))
        
        if starttime.date() <= tempdate <= endtime.date(): 
            print line
            output.write(line)
            output.write("\n")
    
    
    output.seek(0)
    return send_file(output, attachment_filename="testing.txt", as_attachment=True)
    
def create_output():
    pass

@app.route('/')
def init():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
