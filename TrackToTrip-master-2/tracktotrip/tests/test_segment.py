import gpxpy
import unittest
import logging
from tracktotrip import Point, Segment
from datetime import datetime, timedelta

def loadFile(name):
    return gpxpy.parse(open(name, 'r'))

class TestSegment(unittest.TestCase):
    def test_creation(self):
        s1 = Segment([])
        s2 = Segment([Point( 69, 0, datetime(2015, 11, 28, 23, 50, 59, 342380) )])
        print(s2.points[0].lat)
        s3 = Segment([Point( 400, 1000, datetime(2016, 11, 28, 23, 50, 59, 342380)) ,Point( 400, 1000, datetime(2016, 11, 28, 23, 51, 50, 342380)),Point( 501, 1000,datetime(2017, 11, 28, 20, 50, 10, 342380)),Point( 501, 1000,datetime(2017, 11, 28, 20, 55, 59, 342380)),Point( 500, 1000, datetime(2018, 12, 28, 23, 50, 59, 342380)),Point( 500, 1000, datetime(2018, 12, 28, 23, 55, 59, 342380)), Point( 500, 1000, datetime(2018, 12, 28, 23, 58, 59, 342380)), Point( 501, 1000,datetime(2018, 12, 28, 20, 59, 59, 342380))])
        #print(s2.points[0].get_timestamp())
        #print(s2.points[0].lat)
        s2.merge_and_fit(s3)
        for x in range(1,len(s2.points)):
            s2.points[x].compute_metrics(s2.points[x-1])
            

        #print(s2.points[2].lat)

        x = s2.segment(1,1)
        print(x[0])

        self.assertEqual(len(s1.points), 0)
        self.assertEqual(len(s1.transportation_modes), 0)
        self.assertEqual(s1.location_from, None)
        self.assertEqual(s1.location_to, None)

        self.assertEqual(len(s2.points), 1)
        self.assertEqual(len(s2.transportation_modes), 0)
        self.assertEqual(s2.location_from, None)
        self.assertEqual(s2.location_to, None)

    def test_to_json(self):
        time = datetime.now()
        dt = timedelta(1000)

        s = Segment([Point( 0, 0, time), Point( 0, 1, time + dt), Point(0, 2, time + dt)])

        json = s.to_json()
        self.assertTrue('points' in json)
        self.assertTrue('transportationModes' in json)
        self.assertTrue('locationFrom' in json)
        self.assertTrue('locationTo' in json)

if __name__ == '__main__':
    unittest.main()
