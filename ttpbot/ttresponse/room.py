
class Room(object):

    def __init__(self, data):
        for k, v in data.iteritems():
            self.__setattr__(k, v)

            # flaten the meta data into the object
            if k == 'metadata':
                for key, value in v.iteritems():
                    self.__setattr__(key, value)
