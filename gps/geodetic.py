#!/usr/bin/env python

__author__ = 'berglund'

import utilities


class Point(object):

    def __init__(self, x=0.0, y=0.0, z=0.0, cxx=1.0, cyy=1.0, czz=1.0, cxy=0.0, cxz=0.0, cyz=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.cxx = cxx
        self.cyy = cyy
        self.czz = czz
        self.cxy = cxy
        self.cxz = cxz
        self.cyz = cyz

    def __str__(self):
        return "%s %s %s" % (self.x, self.y, self.z)

    def __repr__(self):
        return "geodetic.Point(x=%f,y=%f,z=%f)" % (self.x, self.y, self.z)

    def neu(self, x_ref, y_ref, z_ref):
        """
        Computes the local East North Up components at the specified reference coordinate and rotates the correlation
        matrix.
        Uses:
        1) WGS84 ellipsoid
        2) Topocentric method
        """
        return utilities.xyz2neu(x_ref, y_ref, z_ref, self.x, self.y, self.z) + \
               utilities.covrot(self.x, self.y, self.z, self.cxx, self.cyy, self.czz, self.cxy, self.cxz, self.cyz)

    def neu_globk(self, x_ref, y_ref, z_ref):
        """
        Computes the local East North Up components at the specified reference coordinate and rotates the correlation
        matrix.
        Uses:
        1) WGS84 ellipsoid
        2) GLOBK Method (Tom Herring)
        """
        return utilities.xyz_to_globk_neu(x_ref, y_ref, z_ref, self.x, self.y, self.z) + \
               utilities.covrot(self.x, self.y, self.z, self.cxx, self.cyy, self.czz, self.cxy, self.cxz, self.cyz)


    def llh(self):
        """
        Converts cartesian coordinates to geodetic coordinates.
        """
        return utilities.xyz2llh(self.x, self.y, self.z)


    def xyz(self):
        """
        Returns the point's cartesian coordinates
        """
        return self.x, self.y, self.z

    @staticmethod
    def from_llh(lat, lon, h):
        """
        Construct a cartesian Point object from geodetic coordinates
        """
        x_coord, y_coord, z_coord = utilities.llh2xyz(lat, lon, h)
        return Point(x_coord, y_coord, z_coord)


