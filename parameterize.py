"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 10/22/2016
VERSION: 0.0.3

== Functions ==
+ paramTuple (12/17/2014)
+ paramTupleDebug (12/17/2014)
+ paramComma (12/17/2014)
+ paramKey (12/17/2014)
+ paramDebug (12/17/2014)

TODO:

"""

OPERATORS = ['==', '!=', '<', '<=', '>', '>=']

#paramTuple(self,
#          info)    #Dictionary to parse
# return ("key0, ..., keyX", ":key0, ..., :keyX")
def paramTuple(info):
    keys = ""
    values = ""
    for k in info.keys():
        keys += "{0}, ".format(k)
        values += ":{0}, ".format(k)
    keys = keys[:len(keys)-2]
    values = values[:len(values)-2]
    return (keys, values)

#paramTupleDebug(self,
#                info)    #Dictionary to parse
# return ("key0, ..., keyX", "value0, ..., valueX")
def paramTupleDebug(info):
    keys = ""
    values = ""
    for k in info.keys():
        keys += "{0}, ".format(k)
        values += "{0}, ".format(info[k])
    keys = keys[:len(keys)-2]
    values = values[:len(values)-2]
    return (keys, values)

#paramComma(self,
#          info)    #Dictionary to parse
# return "key0=:key0, ... , keyX=:keyX"
def paramComma(info):
    pairs = ""
    for k in info.keys():
        pairs += "{0}=:{0}, ".format(k)
    pairs = pairs[:len(pairs)-2]
    return pairs

#paramKey(self,
#          info)    #Dictionary to parse
# return "key0<=:key0, key1!=:key1, ... , keyX<:keyX"
def paramKey(info):
    ti = dict(info)
    pairs = ""
    for k in ti.keys():
        if (str(type(ti[k])) != "<type 'tuple'>"):
            pairs += "{0}=:{0} AND ".format(k)
        elif (ti[k][0] in OPERATORS):
            if (ti[k][0] == '!='):
                pairs += "NOT {0}{1}:{0} AND ".format(k, ti[k][0][1])
            elif (ti[k][0] == '=='):
                pairs += "{0}{1}:{0} AND ".format(k, ti[k][0][1])
            else:
                pairs += "{0}{1}:{0} AND ".format(k, ti[k][0])
            ti[k] = ti[k][1]
        else:
            print('{0} is not a valid operator'.format(ti[k][0]))
    pairs = pairs[:len(pairs)-5]
    return (pairs, ti)

#paramDebug(self,
#          info)    #Dictionary to parse
# return "key0<=value0, key1!=value1, ... , keyX<valueX"
def paramDebug(info):
    pairs = ""
    for k in info.keys():
        if (str(type(info[k])) != "<type 'tuple'>"):
            pairs += "{0}=\"{1}\" AND ".format(k, info[k])
        elif (info[k][0] in OPERATORS):
            #String value
            if (type(info[k][1]) is str):
                if (info[k][0] == '!='):
                    pairs += "NOT {0}{1}\"{2}\" AND ".format(k, info[k][0][1], info[k][1])
                elif (info[k][0] == '=='):
                    pairs += "{0}{1}\"{2}\" AND ".format(k, info[k][0][1], info[k][1])
                else:
                    pairs += "{0}{1}\"{2}\" AND ".format(k, info[k][0], info[k][1])
            #Integer value
            else:
                if (info[k][0] == '!='):
                    pairs += "NOT {0}{1}{2} AND ".format(k, info[k][0][1], info[k][1])
                elif (info[k][0] == '=='):
                    pairs += "{0}{1}{2} AND ".format(k, info[k][0][1], info[k][1])
                else:
                    pairs += "{0}{1}{2} AND ".format(k, info[k][0], info[k][1])
        else:
            print('{0} is not a valid operator'.format(info[k][0]))
    pairs = pairs[:len(pairs)-5]
    return pairs