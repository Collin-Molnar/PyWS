'''
Created on Jun 10, 2015

@author: molnar
'''

import datetime

ISO_8601 = "%Y-%m-%dT%H:%M:%S"


def convert_to_iso_8601(epoch):
    return epoch.strftime(ISO_8601)
