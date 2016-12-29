#!/usr/bin/env python
#pylint: skip-file

import pytest
import random
import string

def RandomString():
    return "".join(random.choice(string.ascii_letters + string.digits + string.punctuation + " ") for i in xrange(random.randint(1, 32)))

def RandomKeyword():
    return "a" + "".join(random.choice(string.ascii_letters + string.digits) for i in xrange(random.randint(1, 32)))

def RandomInt():
    return random.randint(-10000, 10000)

def RandomBool():
    return random.choice([True, False])

def Nothing():
    return None

def RandomThing():
    things = [
        RandomInt,
        RandomString,
        RandomBool,
        Nothing,
        str
    ]
    return random.choice(things)()

def CreateTestData():
    """ Create a dictionary of random data """
    keys = [RandomThing() for _ in xrange(10)]
    values = []
    while True:    
        while True:
            t = RandomThing()
            if t not in keys and t not in values:
                break
        values.append(t)
        if len(values) == len(keys):
            break

    return dict(zip(keys, values))

def CreateTestDictStringKeys():
    """ Create a dictionary of random data """
    keys = [RandomString() for _ in xrange(10)]
    values = []
    while True:    
        while True:
            t = RandomThing()
            if t not in keys and t not in values:
                break
        values.append(t)
        if len(values) == len(keys):
            break

    return dict(zip(keys, values))

def TestMap(inputData, outputMap):
    """ Test that outputMap has all of the data from inputData """
    assert len(inputData) == len(outputMap)
    for key, value in inputData.iteritems():
        assert key in outputMap
        assert outputMap[key] == value
        assert outputMap.get(key) == value
        assert value in outputMap
        assert outputMap[value] == key
        assert outputMap.get(value) == key


class Test_TwoWayMap(object):

    def test_init(self):
        print
        from twowaymap import TwoWayMap

        # Random test data
        dd = CreateTestData()

        # Create an empty map
        t = TwoWayMap()
        TestMap({}, t)

        # Create a map from a dictionary
        t = TwoWayMap(dd)
        print "dd = {}".format(dd)
        print " t = {}".format(t)
        TestMap(dd, t)

        # Create a map from a list of tuples
        t = TwoWayMap(zip(dd.keys(), dd.values()))
        print "dd = {}".format(dd)
        print " t = {}".format(t)
        TestMap(dd, t)

        # Create a map from a list of keyword args
        # keyword args must be strings
        dd = CreateTestDictStringKeys()
        t = TwoWayMap(**dd)
        print "dd = {}".format(dd)
        print " t = {}".format(t)
        TestMap(dd, t)

    def test_repr(self):
        print
        from twowaymap import TwoWayMap

        # Random test data
        dd = CreateTestData()
        t = TwoWayMap(dd)
        print str(t)
        print repr(t)

    def test_getsetdel(self):
        print
        from twowaymap import TwoWayMap
        
        t = TwoWayMap()
        key = RandomString()
        value = RandomThing()
        t[key] = value

        key2 = RandomString()
        value2 = RandomThing()
        t[key2] = value2

        assert key in t
        assert t[key] == value
        assert t[value] == key

        assert key2 in t
        assert t[key2] == value2
        assert t[value2] == key2

        del t[key]
        assert key not in t
        assert key2 in t
        assert t[key2] == value2
        assert t[value2] == key2

    def test_iteration(self):
        print
        from twowaymap import TwoWayMap

        # Random test data
        dd = CreateTestData()
        t = TwoWayMap(dd)

        count = 0
        for k in iter(t):
            v = t[k]
            assert(dd[k] == v)
            assert(t[v] == k)
            count += 1
        assert len(t) == count

        count = 0
        for k, v in t.iteritems():
            assert(dd[k] == v)
            count += 1
        assert len(t) == count

        count = 0
        for k, v in t.items():
            assert(dd[k] == v)
            count += 1
        assert len(t) == count

        count = 0
        for k in t.iterkeys():
            v = t[k]
            assert(dd[k] == v)
            assert(t[v] == k)
            count += 1
        assert len(t) == count

        count = 0
        for k in t.keys():
            v = t[k]
            assert(dd[k] == v)
            assert(t[v] == k)
            count += 1
        assert len(t) == count

        count = 0
        for v in t.itervalues():
            k = t[v]
            assert(dd[k] == v)
            assert(t[k] == v)
            count += 1
        assert len(t) == count

        count = 0
        for v in t.values():
            k = t[v]
            assert(dd[k] == v)
            assert(t[k] == v)
            count += 1
        assert len(t) == count
