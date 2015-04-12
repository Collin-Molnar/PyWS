'''
Created on Mar 18, 2015

@author: molnar
'''
from StringIO import StringIO
import ftplib
from ftplib import FTP
import geodetic

class ProcessPos:
    
    def __init__(self, posFile):
        self.get_file(posFile)
    
    def get_file(self, posfile):
        ftp = FTP('data-out.unavco.org')
        ftp.login()
        r = StringIO()
        
        try:
            ftp.retrbinary('RETR ' + posfile, r.write)
        except ftplib.all_errors:
            print "ERROR with FTP"
            
        posfile = r.getvalue()
        lines = posfile.splitlines()
        
        self.output = ""
        
        for i, line in enumerate(lines):
            
            if i == 7:
                ref_xyz = tuple([float(j) for j in line.split()[4:7]])
                print 'REF XYZ'
                print ref_xyz
                
            elif i == 8:
                ref_llh = tuple([float(j) for j in line.split()[4:7]])
                print "REF LLH"
                print ref_llh
                
            elif i > 36:
                dataline = [float(j) for j in line.split() if self.is_number(j)]
                dataline.append(line.split()[24])
                point = tuple(dataline[3:12])
                P1 = geodetic.Point(*point)
                # (N, E, U, sigma_E, sigma_N, sigma_U, EN corr, EU corr, NU corr)
                test_neu = P1.neu(*ref_xyz)
            
                self.output += "{0:<125}{1[0]:<15.10f}{1[1]:<15.10f}{1[1]:<15.10f}{1[4]:<15.10f}{1[3]:<15.10f}{1[5]:<15.10f}{1[6]:<15.10f}{1[8]:<15.10f}{1[7]:<15.10f}{2:}".format(line[:120], test_neu, dataline[24])
            
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
    
#     get_file(posfile)
                    
        


    