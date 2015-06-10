'''
Created on Mar 18, 2015

@author: molnar
'''
import StringIO
import datetime
import ftplib
import urllib2
from ftplib import FTP
from geodetic import geodetic
from util import datetime_util
from test import test_new

UNR_TS_FORMAT = "%Y-%m-%d %H:%M:%S"

class ProcessPos:
        
    def __init__(self, file_location, short = True):
        self.short = short
        self.file = file_location
    
    def start_unr_process(self, ref_frame, strt_time, end_time):
        self.reference_frame = ref_frame
        self.strt_time = strt_time
        self.end_time = end_time
        
        response = urllib2.urlopen(self.file)
        gsac_return = response.read()
        lines = self.get_unr_file_name(gsac_return)
        return self.output
        
    def get_unr_file_name(self, gsac_return):
        for line in gsac_return.split("\n"):
            if "#" in line:
                continue
            elif(line != ""):
                self.file_strt_time = datetime.datetime.strptime(line.split(",")[6], UNR_TS_FORMAT)
                self.file_end_time = datetime.datetime.strptime(line.split(",")[7], UNR_TS_FORMAT)
                
                # Get file name from the 5th object in csv line.
                # Then split on '/' to get neu/xyz and ref frame.
                # Then grab coord_type from the 4th and 5th index. 
                file_url = line.split(",")[5]
                coord_type, file_ref_frame = file_url.split("/")[4:6]
                
                if (coord_type == "txyz" and file_ref_frame.lower() == self.reference_frame):
                    self.get_unr_file(file_url) 
                    return  
                    
    def get_unr_file(self, file_url):
        response = urllib2.urlopen(file_url)
        html = response.read()
        self.process_unr_file(html)
     
    def process_unr_file(self, html):
        """
        ------------
        .txyz2 format (x,y,z time series)
        ------------
        1. station ID (SSSS)
        2. date (yymmmdd)
        3. decimal year
        4. x (m)
        5. y (m)
        6. z (m)
        7. sigma x (m)
        8. sigma y (m)
        9. sigma z (m)
        10. correlation xy
        11. correlation yz
        12. correlation xz
        13. antenna height (m)
        """   
        self.output = "" 
        for i, line in enumerate(html.split("\n")): 
            parts = line.split()
            # Last line of file is empty item in list
            if len(parts) == 0:
                break
            if i == 0:
                ref_xyz = parts[3:6]
                ref_xyz = [float(i) for i in ref_xyz]
                self.output += str(ref_xyz) + "\n"
            line_date = datetime.datetime.strptime(parts[1], "%y%b%d")
            if self.strt_time <= line_date <= self.end_time:
                x = float(parts[3])
                y = float(parts[4])
                z = float(parts[5])
                sig_x = float(parts[6])
                sig_y = float(parts[7])
                sig_z = float(parts[8])
                corr_xy = float(parts[9])
                corr_xz = float(parts[10])
                corr_yz = float(parts[11])
                
                #(X,Y,Z,StdDev x, StdDev y, StdDev z, corr xy, corr xy, corr yz)
                point = (x, y, z, sig_x, sig_y, sig_z, corr_xy, corr_xz, corr_yz)
                P1 = geodetic.Point(*point)
                
                test_neu = P1.neu(*ref_xyz)
                # Both short and long start off with the datetime. 
                self.output += "{} ".format(datetime_util.convert_to_iso_8601(line_date))
                # Convert the m neu to mm
                test_neu = [x * 1000 for x in test_neu]
                if self.short:
                    ###############       N             E            U            Sig N         Sig E         Sig U   Solution
                    self.output += "{0[0]:<20.15f}{0[1]:<20.15f}{0[2]:<20.15f}{0[3]:<20.15f}{0[4]:<20.15f}{0[5]:<20.15f}{1}\n".format(test_neu, "UNR")
                else: 
                    self.output += "{0:<125}{1[0]:<15.10f}{1[1]:<15.10f}{1[1]:<15.10f}{1[4]:<15.10f}{1[3]:<15.10f}{1[5]:<15.10f}{1[6]:<15.10f}{1[8]:<15.10f}{1[7]:<15.10f}{2:}\n".format(line[23:120], test_neu, "UNR")
            
                
    def get_unavco_file(self):
        ftp = FTP('data-out.unavco.org')
        ftp.login()
        r = StringIO.StringIO()
        
        try:
            ftp.retrbinary('RETR ' + self.file, r.write)
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
                # TODO: Document Geodetic 
                # POS FILE
                epoch = line.split[0]
                print epoch
                dataline = [float(j) for j in line.split() if self.is_number(j)]
                # Append solution
                dataline.append(line.split()[24])
                
                #(X,Y,Z,StdDev x, StdDev y, StdDev z, corr xy, corr xy, corr yz)
                point = tuple(dataline[3:12])
                
                P1 = geodetic.Point(*point)
                # (N, E, U, sigma_E, sigma_N, sigma_U, EN corr, EU corr, NU corr)
                test_neu = P1.neu(*ref_xyz)
                if not self.short:
                    # TODO document long
                    self.output += "{0:<125}{1[0]:<15.10f}{1[1]:<15.10f}{1[1]:<15.10f}{1[4]:<15.10f}{1[3]:<15.10f}{1[5]:<15.10f}{1[6]:<15.10f}{1[8]:<15.10f}{1[7]:<15.10f}{2:}\n".format(line[:120], test_neu, dataline[24])
                else: 
                    # TODO update short
                    self.output += "TEST"
        ftp.close()
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
                    
        


    