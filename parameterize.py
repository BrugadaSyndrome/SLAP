"""
AUTHOR: COBY JOHNSON
PROJECT: SLAP (Sql-Lite wrApper in Python)
LAST UPDATE: 5/3/2014
VERSION: 0.0.2

DONE:
+ paramTuple (5/3/2014)
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
    pairs = ""
    for k in info.keys():
        if (str(type(info[k])) != "<type 'tuple'>"):
            pairs += k + "=:" + k + " AND "
        elif (info[k][0] in OPERATORS):
            if (info[k][0] == '!='):
                pairs += "NOT " + k + info[k][0][1] + ":" + k + " AND "
            elif (info[k][0] == '=='):
                pairs += k + info[k][0][1] + ":" + k + " AND "
            else:
                pairs += k + info[k][0] + ":" + k + " AND "
            info[k] = info[k][1]
        else:
            print '{0} is not a valid operator'.format(info[k][0])
    pairs = pairs[:len(pairs)-5]
    return pairs

#paramDebug(self,
#          info)    #Dictionary to parse
# return "key0<=value0, key1!=value1, ... , keyX<valueX"
def paramDebug(info):
    pairs = ""
    for k in info.keys():
        if (str(type(info[k])) != "<type 'tuple'>"):
            if (type(info[k]) is str):
                pairs += k + '="' + info[k] + '" AND '
            else:
                pairs += k + '=' + str(info[k]) + ' AND '
        #String value
        elif (type(info[k][1]) is str):
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
    pairs = pairs[:len(pairs)-5]
    return pairs