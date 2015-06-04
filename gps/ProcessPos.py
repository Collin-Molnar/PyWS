'''
Created on Mar 18, 2015

@author: molnar
'''
from StringIO import StringIO
from datetime import datetime
import ftplib
import urllib2
from ftplib import FTP
from geodetic import geodetic

UNR_TS_FORMAT = "%Y-%m-%d %H:%M:%S"

class ProcessPos:
        
    def __init__(self, file_location):
        self.file = file_location
    
    def process_unr(self, ref_frame, strt_time, end_time):
        self.reference_frame = ref_frame
        self.strt_time = strt_time
        self.end_time = end_time
        
        response = urllib2.urlopen(self.file)
        gsac_return = response.read()
        lines = self.get_unr_file_name(gsac_return)
        print lines
        
    def get_unr_file_name(self, gsac_return):
        for line in gsac_return.split("\n"):
            if "#" in line:
                continue
            elif(line != ""):
                file_strt_time = datetime.strptime(line.split(",")[6], UNR_TS_FORMAT)
                file_end_time = datetime.strptime(line.split(",")[7], UNR_TS_FORMAT)
                
                # Get file name from the 5th object in csv line.
                # Then split on '/' to get neu/xyz and ref frame.
                # Then grab coord_type from the 4th and 5th index. 
                file_url = line.split(",")[5]
                coord_type, file_ref_frame = file_url.split("/")[4:6]
                
                if (coord_type == "txyz" and file_ref_frame.lower() == self.reference_frame):
                    print file_url
                    self.get_unr_file(file_url)   
                    
    def get_unr_file(self, file_url):
        response = urllib2.urlopen(file_url)
        html = response.read()
        print html
        
    def get_unavco_file(self):
        ftp = FTP('data-out.unavco.org')
        ftp.login()
        r = StringIO()
        
        try:
            ftp.retrbinary('RETR ' + posfile, r.write)
        except ftplib.all_errors as f:
            print "ERROR with FTP"
            print f
            
        posfile = r.getvalue()
        lines = posfile.splitlines()
        
        self.output = ""
        
        for i, line in enumerate(lines):
            
            if i == 7:
                ref_xyz = tuple([float(j) for j in line.split()[4:7]])
                self.output += str(ref_xyz) + "\n"
              
            elif i == 8:
                ref_llh = tuple([float(j) for j in line.split()[4:7]])
                
            elif i > 36:
                # TODO: 
                dataline = [float(j) for j in line.split() if self.is_number(j)]
                dataline.append(line.split()[24])
                point = tuple(dataline[3:12])
                P1 = geodetic.Point(*point)
                # (N, E, U, sigma_E, sigma_N, sigma_U, EN corr, EU corr, NU corr)
                test_neu = P1.neu(*ref_xyz)
                self.output += "{0:<125}{1[0]:<15.10f}{1[1]:<15.10f}{1[1]:<15.10f}{1[4]:<15.10f}{1[3]:<15.10f}{1[5]:<15.10f}{1[6]:<15.10f}{1[8]:<15.10f}{1[7]:<15.10f}{2:}\n".format(line[:120], test_neu, dataline[24])
            
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def getoutput(self):
        return self.output
          
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="The the position file to process")
    args = parser.parse_args()
    
    posfile = args.file
    
#     get_unavco_file(posfile)
                    
        


    