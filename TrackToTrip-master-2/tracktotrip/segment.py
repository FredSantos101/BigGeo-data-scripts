"""
Point segment module
"""
from copy import deepcopy
import sys
import traceback

import numpy as np

from .point import Point
from .utils import pairwise
from .smooth import with_no_strategy, with_extrapolation, with_inverse
from .smooth import NO_STRATEGY, INVERSE_STRATEGY, EXTRAPOLATE_STRATEGY
from .location import infer_location
from .similarity import sort_segment_points, closest_point
from .compression import spt, drp
from .transportation_mode import speed_clustering
from .spatiotemporal_segmentation import spatiotemporal_segmentation


def remove_liers(points):
    """ Removes obvious noise points
    Checks time consistency, removing points that appear out of order
    Args:
        points (:obj:`list` of :obj:`Point`)
    Returns:
        :obj:`list` of :obj:`Point`
    """
    if (108.0<= points[0].lon <= 125.0 and 35 <= points[0].lat <= 45):
        print("The longitude is: " + str(points[0].lon) + " and the lat: " + str(points[0].lat))
        result = [points[0]]
    else:
        result = []
    for i in range(1, len(points) - 2):
        prv = points[i-1]
        crr = points[i]
        nxt = points[i+1]
        if (prv.time <= crr.time and crr.time <= nxt.time and 108.0<= crr.lon and crr.lon <= 125.0 and 35 <= crr.lat and crr.lat <= 45 and crr.vel <= 160.0):           
            print("The longitude is: " + str(crr.lon) + " and the lat: " + str(crr.lat))
            result.append(crr)
    result.append(points[-1])

    return result

def remove_OutLiers_Time_Vel(points):
    """ Removes obvious noise points

    Checks time consistency, removing points that appear out of order

    Args:
        points (:obj:`list` of :obj:`Point`)
    Returns:
        :obj:`list` of :obj:`Point`
    """

    print("ok im here")
    result = []
    cont = 0
    firstTime = True
    if len(points) >= 3:
        for i in range(1, len(points) - 1):
            prv = points[i-1]
            crr = points[i]
            nxt = points[i+1]
            
            if prv.time < crr.time and crr.time < nxt.time:
                if firstTime:
                    firstTime = False
                    if crr.vel <= 150 and (prv.lon <= 124.0 and prv.lon >= 110.0 and prv.lat >= 36.0 and prv.lat <= 43.0):
                        result.append(prv) 
                        result.append(crr) 
                elif not (crr.lon <= 124.0 and crr.lon >= 110.0 and crr.lat >= 36.0 and crr.lat <= 43.0 and crr.vel < 150):
                    print("Inside the bounds and velocity threshold AND MY VEL IS:")
                    print(crr.vel)
                    cont += 1
                    points[i+1].compute_metrics(prv)

                
                elif (crr.vel < 150):
                    if abs(crr.vel - prv.vel) < 70:
                        print("Should have less than 150 but it is:")
                        print(crr.vel)
                        result.append(crr) 
                

                else:
                    cont += 1
                    points[i+1].compute_metrics(prv)
        if(points[-1].vel> 150):
            result.append(points[-1])
        print("Noise removal took care of: " + str(cont))
    return result



class Segment(object):
    """Holds the points and semantic information about them

    Attributes:
        points (:obj:`list` of :obj:`Point`): points of the segment
        #TODO
        transportation_modes: array of transportation modes of the segment
            Each transportation mode represents a span of points
            Each span is a map in the following format:
                label: string with the type of transportation mode
                from: start of the span
                to: end of the span
        locationFrom: TrackToTrip.Location or None, the semantic location of
            the start of the segment
        locationTo: TrackToTrip.Location or None, the semantic location of
            the end of the segment
    """

    def __init__(self, points):
        self.points = points
        self.transportation_modes = []
        self.location_from = None
        self.location_to = None

    def bounds(self, thr=0, lower_index=0, upper_index=-1):
        """ Computes the bounds of the segment, or part of it

        Args:
            lower_index (int, optional): Start index. Defaults to 0
            upper_index (int, optional): End index. Defaults to 0
        Returns:
            :obj:`tuple` of :obj:`float`: Bounds of the (sub)segment, such that
                (min_lat, min_lon, max_lat, max_lon)
        """
        points = self.points[lower_index:upper_index]

        min_lat = float("inf")
        min_lon = float("inf")
        max_lat = -float("inf")
        max_lon = -float("inf")

        for point in points:
            min_lat = min(min_lat, point.lat)
            min_lon = min(min_lon, point.lon)
            max_lat = max(max_lat, point.lat)
            max_lon = max(max_lon, point.lon)

        return (min_lat - thr, min_lon - thr, max_lat + thr, max_lon + thr)

    def remove_noise(self):
        """In-place removal of noise points

        See `remove_noise` function

        Returns:
            :obj:`Segment`
        """
        print("Removeing outliers in Segment")
        self.points = remove_liers(self.points)
        return self

    def smooth(self, noise, strategy):
        """ In-place smoothing

        See smooth_segment function

        Args:
            noise (float): Noise expected
            strategy (str): Strategy to use. Either smooth.INVERSE_STRATEGY
                or smooth.EXTRAPOLATE_STRATEGY
        Returns:
            :obj:`Segment`
        """
        print("Im in the smooth function")
        
        if strategy == INVERSE_STRATEGY:
            print("Im inversing")
            self.points = with_inverse(self.points, noise)
        elif strategy == EXTRAPOLATE_STRATEGY:
            print("Im extrapolating")
            self.points = with_extrapolation(self.points, noise, 30)
        elif strategy == NO_STRATEGY:
            print("Im not applying any strategy")
            self.points = with_no_strategy(self.points, noise)
        return self

    def segment(self, eps, min_time):
        """Spatio-temporal segmentation

        See spatiotemporal_segmentation function

        Args:
            eps (float): Maximum distance between two samples
            min_time (float): Minimum time between to segment
        Returns:
            :obj:`list` of :obj:`Point`
        """

        return spatiotemporal_segmentation(self.points, eps, min_time)

    def simplify(self, eps, max_dist_error, max_speed_error, topology_only=False):
        """ In-place segment simplification

        See `drp` and `compression` modules

        Args:
            eps (float): Distance threshold for the `drp` function
            max_dist_error (float): Max distance error, in meters
            max_speed_error (float): Max speed error, in km/h
            topology_only (bool, optional): True to only keep topology, not considering
                times when simplifying. Defaults to False.
        Returns:
            :obj:`Segment`
        """
        if topology_only:
            self.points = drp(self.points, eps)
        else:
            self.points = spt(self.points, max_dist_error, max_speed_error)
        return self

    def compute_metrics(self):
        """ Computes metrics for each point

        Returns:
            :obj:`Segment`: self
        """
        for prev, point in pairwise(self.points):
            point.compute_metrics(prev)
        return self

    def infer_location(
            self,
            location_query,
            max_distance,
            google_key,
            foursquare_client_id,
            foursquare_client_secret,
            limit
        ):
        """In-place location inferring

        See infer_location function

        Args:
        Returns:
            :obj:`Segment`: self
        """

        self.location_from = infer_location(
            self.points[0],
            location_query,
            max_distance,
            google_key,
            foursquare_client_id,
            foursquare_client_secret,
            limit
        )
        self.location_to = infer_location(
            self.points[-1],
            location_query,
            max_distance,
            google_key,
            foursquare_client_id,
            foursquare_client_secret,
            limit
        )

        return self

    def infer_transportation_mode(self, clf, min_time):
        """In-place transportation mode inferring

        See infer_transportation_mode function

        Args:
        Returns:
            :obj:`Segment`: self
        """
        self.transportation_modes = speed_clustering(clf, self.points, min_time)
        return self

    def merge_and_fit(self, segment):
        """ Merges another segment with this one, ordering the points based on a
            distance heuristic

        Args:
            segment (:obj:`Segment`): Segment to merge with
        Returns:
            :obj:`Segment`: self
        """
        self.points = sort_segment_points(self.points, segment.points)
        return self
    
    #only append at the end 
    # REQIRES ORDERED INPUT
    def add_point_end_of_segment(self, Pnt):
        """Takes one line segment and a point and connects it
        first's end

        Args:
            Aps: Array of tracktotrip.Point
            Pnt: New Point of tracktotrip.Point
        Returns:
            Array with point included in the end
        """
        self.points.append(Pnt)

    def closest_point_to(self, point, thr=20.0):
        """ Finds the closest point in the segment to a given point

        Args:
            point (:obj:`Point`)
            thr (float, optional): Distance threshold, in meters, to be considered
                the same point. Defaults to 20.0
        Returns:
            (int, Point): Index of the point. -1 if doesn't exist. A point is given if it's along the segment

        """
        i = 0
        point_arr = point.gen2arr()

        def closest_in_line(pointA, pointB):
            temp = closest_point(pointA.gen2arr(), pointB.gen2arr(), point_arr)
            return Point(temp[1], temp[0], None)

        for (p_a, p_b) in pairwise(self.points):
            candidate = closest_in_line(p_a, p_b)
            if candidate.distance(point) <= thr:
                if p_a.distance(point) <= thr:
                    return i, p_a
                elif p_b.distance(point) <= thr:
                    return i + 1, p_b
                else:
                    return i, candidate
            i = i + 1
        return -1, None

    def slice(self, start, end):
        """ Creates a copy of the current segment between indexes. If end > start,
            points are reverted

        Args:
            start (int): Start index
            end (int): End index
        Returns:
            :obj:`Segment`
        """

        reverse = False
        if start > end:
            temp = start
            start = end
            end = temp
            reverse = True

        seg = self.copy()
        seg.points = seg.points[start:end+1]
        if reverse:
            seg.points = list(reversed(seg.points))

        return seg

    def copy(self):
        """ Creates a deep copy of this instance

        Returns:
            :obj:`Segment`
        """
        return deepcopy(self)

    def to_json(self):
        """ Converts segment to a JSON serializable format

        Returns:
            :obj:`dict`
        """
        points = [point.to_json() for point in self.points]
        return {
            'points': points,
            'transportationModes': self.transportation_modes,
            'locationFrom': self.location_from.to_json() if self.location_from != None else None,
            'locationTo': self.location_to.to_json() if self.location_to != None else None
        }

    @staticmethod
    def from_gpx(gpx_segment):
        """ Creates a segment from a GPX format.

        No preprocessing is done.

        Arguments:
            gpx_segment (:obj:`gpxpy.GPXTrackSegment`)
        Return:
            :obj:`Segment`
        """
        points = []
        for point in gpx_segment.points:
            points.append(Point.from_gpx(point))
        return Segment(points)

    @staticmethod
    def from_json(json):
        """ Creates a segment from a JSON file.

        No preprocessing is done.

        Arguments:
            json (:obj:`dict`): JSON representation. See to_json.
        Return:
            :obj:`Segment`
        """
        points = []
        for point in json['points']:
            points.append(Point.from_json(point))
        return Segment(points)
