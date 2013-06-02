
class Speak(object):
    """ Object used to represent when a user Speaks from response data.  This
    object's members can be "dot" accessed as long as their present.  It is
    assumed that user data is consistent.

    TODO: This object could use a better name
    """
    def __init__(self, data):
        """
            {
                u'userid': u'51a3f228aaa5cd45fe2669fb',
                u'command': u'speak',
                u'name': u'johncosta+ttbot',
                u'roomid': u'4f47e169590ca24b66002684',
                u'text': u'Hi {0}'
            }
        """
        for k, v in data.iteritems():
            self.__setattr__(k, v)
