#!/usr/bin/env python
#pylint: skip-file

from pprint import pformat
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

def CreateUniqueList(randFunc, length, exclusions=None):
    exclusions = exclusions or []
    values = []
    while len(values) < length:
        t = randFunc()
        if t in values or t in exclusions:
            continue
        values.append(t)
    return values

def CreateTestDictionary(keyGenerator=RandomThing, valueGenerator=RandomThing, length=20):
    keys = CreateUniqueList(keyGenerator, length)
    values = CreateUniqueList(valueGenerator, length, keys)
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
        if isinstance(key, basestring):
            assert getattr(outputMap, key) == value


class Test_TwoWayMap(object):

    def test_init(self):
        print
        from twowaymap import TwoWayMap

        # Random test data
        dd = CreateTestDictionary()
        print "dd = {}".format(pformat(dd))

        # Create an empty map
        t = TwoWayMap()
        TestMap({}, t)

        # Create a map from a dictionary
        t = TwoWayMap(dd)
        print " t = {}".format(t)
        TestMap(dd, t)

        # Create a map from a list of tuples
        t = TwoWayMap(zip(dd.keys(), dd.values()))
        print " t = {}".format(t)
        TestMap(dd, t)

        # Create a map from a list of keyword args
        # keyword args must be strings
        dd = CreateTestDictionary(keyGenerator=RandomString)
        t = TwoWayMap(**dd)
        print " t = {}".format(t)
        TestMap(dd, t)

    def test_repr(self):
        print
        from twowaymap import TwoWayMap

        # Random test data
        dd = CreateTestDictionary()
        t = TwoWayMap(dd)
        print str(t)
        print repr(t)

    def test_getsetdelclear(self):
        print
        from twowaymap import TwoWayMap

        test_keys = CreateUniqueList(RandomThing, 2)
        test_vals = CreateUniqueList(RandomThing, 2, test_keys)

        t = TwoWayMap()

        t[test_keys[0]] = test_vals[0]
        print " t = {}".format(t)
        assert len(t) == 1

        t[test_keys[1]] = test_vals[1]
        print " t = {}".format(t)
        assert len(t) == 2

        for idx in xrange(2):
            assert test_keys[idx] in t
            assert t[test_keys[idx]] == test_vals[idx]
            assert t[test_vals[idx]] == test_keys[idx]

        del t[test_keys[0]]
        print " t = {}".format(t)
        assert len(t) == 1
        assert test_keys[0] not in t
        assert test_keys[1] in t
        assert t[test_keys[1]] == test_vals[1]
        assert t[test_vals[1]] == test_keys[1]

        dd = CreateTestDictionary(length=10)
        t = TwoWayMap(dd)
        assert len(t) == len(dd)
        t.clear()
        assert len(t) == 0
        assert len(dd) == 10

    def test_duplicatekeyvals(self):
        print
        from twowaymap import TwoWayMap

        data = CreateUniqueList(RandomString, 4)

        t = TwoWayMap()

        # Identical keys are allowed, they just overwrite each other
        t[data[0]] = data[1]
        t[data[0]] = data[2]
        print "t  = {}".format(t)
        assert len(t) == 1
        assert t[data[0]] == data[2]
        t.clear()

        # Overwriting a key/value with itself is allowed
        t[data[0]] = data[1]
        t[data[0]] = data[1]
        print "t  = {}".format(t)
        assert len(t) == 1
        t.clear()

        # Identical values with different keys are not allowed
        t[data[0]] = data[1]
        print "t  = {}".format(t)
        with pytest.raises(ValueError):
            t[data[2]] = data[1]
        assert len(t) == 1
        t.clear()

        # New values that are the same as existing keys are not allowed
        t[data[0]] = data[1]
        print "t  = {}".format(t)
        with pytest.raises(ValueError):
            t[data[2]] = data[0]
        assert len(t) == 1
        t.clear()

        # Overwriting existing values with an overlapping value is not allowed
        t[data[0]] = data[1]
        t[data[2]] = data[3]
        print "t  = {}".format(t)
        with pytest.raises(ValueError):
            t[data[0]] = data[3]
        assert len(t) == 2

        # Overwriting existing values with a value the same as an existing key is not allowed
        t[data[0]] = data[1]
        t[data[2]] = data[3]
        print "t  = {}".format(t)
        with pytest.raises(ValueError):
            t[data[0]] = data[2]
        assert len(t) == 2

    def test_iteration(self):
        print
        from twowaymap import TwoWayMap

        # Random test data
        dd = CreateTestDictionary()
        t = TwoWayMap(dd)

        print "dd = {}".format(pformat(dd))
        print "t  = {}".format(t)

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
