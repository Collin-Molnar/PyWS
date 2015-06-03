#!flask/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 11, 2015

@author: molnar
'''
from flask import Flask, request, send_file
import StringIO
import ProcessPos
import datetime
from util import validator
from util.validator import check_ref_frame, check_analysis_center,\
    check_ts_format
import geodetic
from Canvas import Line


app = Flask(__name__)
output = StringIO.StringIO()

@app.route('/gps/data/position/<station>/v2')
def gps(station):
    '''
    http://127.0.0.1:5000/gps/data/position/P378/v2?referenceFrame=igs08&analysisCenter=pbo&starttime=2012-01-01T00%3A00%3A00&endtime=2012-01-02T00%3A00%3A00&tsFormat=iso8601&stdDevRange=false
    '''
    #########################################################
    # Get query parameters
    #########################################################
    reference_frame = request.args.get('referenceFrame')         # nam08
    if not check_ref_frame(reference_frame):
        pass
        # TODO: Create errors 
        
    analysis_center = request.args.get('analysisCenter')         # pbo
    if not check_analysis_center(analysis_center):
        pass
        # TODO: Create errors 
    
    ts_format = request.args.get('tsFormat')                      # iso8601&
    if not check_ts_format(ts_format):
        pass
        #TODO: Create error 
    
    # TODO: Necesary to validate or just use strp time??
    starttime = request.args.get('starttime')                    # 2006-01-01T00%3A00%3A00&
    endtime = request.args.get('endtime')                        # 2012-03-01T00%3A00%3A00&
    
    stdDevRange = request.args.get('std_dev_range')              # false
    
    ARCHIVE_POS_LOCS = "pub/products/position"
    ISO_8601 = "%Y-%m-%dT%H:%M:%S"
    
    starttime = datetime.datetime.strptime(starttime, ISO_8601)
    endtime = datetime.datetime.strptime(endtime, ISO_8601)
    
 
    
    # Position file location
    file_location = ARCHIVE_POS_LOCS + "/" + station + "/" + station + "." + analysis_center + "." + reference_frame + ".pos"
    pp = ProcessPos.ProcessPos(file_location)
    result = pp.getoutput().splitlines()
    
    # Get reference corrdinate from first line to pass to header. 
    ref_xyz = result[0]
    
    path = request.path
    
    print_header(ref_xyz, path)
    
    for i, line in enumerate(result):
        # Get the date at the beginning of the line and put into a datetime object.
        # First line contain ref coord. 
        if i == 0:
            continue
          
        tempdate = line.split()[0]
        tempdate = datetime.date(int(tempdate[:4]), int(tempdate[4:6]), int(tempdate[6:]))
#         print "START: " + str(starttime.date())
#         print "TEMP: " + str(tempdate)
#         print "END: " + str(endtime.date())
        if starttime.date() <= tempdate <= endtime.date(): 

            if (ts_format.lower() == 'unixepochms'):
                returnline = str(tempdate.strftime("%s "))
                returnline += line[9:]
            else:
                returnline = line    
            output.write(returnline)
            print returnline
            output.write("\n")

     
    # Set the files position cursor to the beginning. 
    output.seek(0)
    return send_file(output, attachment_filename="testing.txt", as_attachment=True)

def print_header(ref_xyz, path):
        output.write("# fields: DateTime, X, Y, Z, X Std. Dev, Y Std. Dev, Z Std. Dev, XY Correlation, XZ Correlation, YZ Correlation, North Latitude, East Longitude, Height,  North, East, Vertical, North Std. Dev.(m), East Std. Dev.(m), Vertical Std. Dev.(m), NorthEast Correlation, NorthVertical Correlation, EastVertical Correlation, Solution")
        output.write("\n")     
        output.write("# f​ield_unit: ISO 8601 datetime UTC, meters, meters, meters, millimeters, millimeters, millimeters, number, number, number, degrees, degrees, meters, meters, meters, meters, meters, meters, meters, number, number, number, UTF-8")
        output.write("\n")
        output.write("# f​ield_type: s​tring, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, string")
        output.write("\n")
        output.write("# attribution: h​ttp:#www.unavco.org/community/policies_forms/attribution/attribution.html")
        output.write("\n")
        
        # Create URL 
        output.write("# url: http:#web-services.unavco.org")
        # TODO: GET URL
        output.write("myURI: ")
        output.write(path)
        output.write("\n")
        
        # Reference Coordinate 
        output.write("# XYZ Reference Coordinate: ")
        output.write(ref_xyz)
        output.write("\n")
        
        print output

@app.route('/')
def init():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
