'''
Created on Jun 2, 2015

@author: molnar
'''
import iso8601

"""
This method is used to see if the reference frame passed in is valid. 

Returns True if it's a valid refernce frame.  
"""
def check_ref_frame(ref_frame):
    list = ["NAM08", "IGS08", "SNF01", "IGS05", "NA12"]
    if ref_frame.upper() in list:
        return True
    else:
        return False
    
"""
This method is used to see if the analysis center passed in is valid. 

Returns True if it's an valid analysis center.  
"""
def check_analysis_center(center):
    list = ["CWU", "NMT", "PBO", "MIT", "UNR"]
    if center.upper() in list: 
        return True
    else:
        return False
"""
Is this necessary with the strptime? 
"""    
def check_date(input_date):
    pass

def check_ts_format(ts_format):
    list = ["iso8601", "unixepochms"]
    if ts_format.lower() in list:
        return True
    else: 
        return False