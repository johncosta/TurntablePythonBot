class Room(object):
    """ Object used to represent a room from response data.  This objects
    members can be "dot" accessed as long as their present. The assumption
    is that Room data is consistent.
    """
    def __init__(self, data):
        for k, v in data.iteritems():
            self.__setattr__(k, v)

            # flaten the meta data into the object
            if k == 'metadata':
                for key, value in v.iteritems():
                    self.__setattr__(key, value)
