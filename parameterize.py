"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 5/4/2014
VERSION: 0.0.2

== Functions ==
+ paramTuple (5/3/2014)
+ paramTupleDebug (5/4/2014)
+ paramComma (5/3/2014)
+ paramKey (5/3/2014)
+ paramDebug (5/3/2014)

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
        keys += k + ", "
        values += ":" + k + ", "
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
        keys += k + ", "
        values += str(info[k]) + ", "
    keys = keys[:len(keys)-2]
    values = values[:len(values)-2]
    return (keys, values)

#paramComma(self,
#          info)    #Dictionary to parse
# return "key0=:key0, ... , keyX=:keyX"
def paramComma(info):
    pairs = ""
    for k in info.keys():
        pairs += k + "=:" + k + ", "
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
            pairs += k + "=:" + k + " AND "
        elif (ti[k][0] in OPERATORS):
            if (ti[k][0] == '!='):
                pairs += "NOT " + k + ti[k][0][1] + ":" + k + " AND "
            elif (ti[k][0] == '=='):
                pairs += k + ti[k][0][1] + ":" + k + " AND "
            else:
                pairs += k + ti[k][0] + ":" + k + " AND "
            ti[k] = ti[k][1]
        else:
            print '{0} is not a valid operator'.format(ti[k][0])
    pairs = pairs[:len(pairs)-5]
    return (pairs, ti)

#paramDebug(self,
#          info)    #Dictionary to parse
# return "key0<=value0, key1!=value1, ... , keyX<valueX"
def paramDebug(info):
    pairs = ""
    for k in info.keys():
        if (str(type(info[k])) != "<type 'tuple'>"):
            #String value
            if (type(info[k]) is str):
                pairs += k + '="' + info[k] + '" AND '
            #Integer Value
            else:
                pairs += k + '=' + str(info[k]) + ' AND '
        elif (info[k][0] in OPERATORS):
            #String value
            if (type(info[k][1]) is str):
                if (info[k][0] == '!='):
                    pairs += "NOT " + k + info[k][0][1] + '"' + info[k][1] + '" AND '
                elif (info[k][0] == '=='):
                    pairs += k + info[k][0][1] + '"' + info[k][1] + '" AND '
                else:
                    pairs += k + info[k][0] + '"' + info[k][1] + '" AND '
            #Integer value
            else:
                if (info[k][0] == '!='):
                    pairs += "NOT " + k + info[k][0][1] + str(info[k][1]) + " AND "
                elif (info[k][0] == '=='):
                    pairs += k + info[k][0][1] + str(info[k][1]) + " AND "
                else:
                    pairs += k + info[k][0] + str(info[k][1]) + " AND "
        else:
            print '{0} is not a valid operator'.format(info[k][0])
    pairs = pairs[:len(pairs)-5]
    return pairs