
class User(object):
    """ Object used to represent a User from response data.  This objects
    members can be "dot" accessed as long as their present.  It is assumed that
    user data is consistent.
    """

    def __init__(self, data):
        """
        data is an arbitrary dictionary of values. We'll assume that the
        caller is passing the correct data that makes a user.  This way we can
        do stuff like user.name vs user.get('name')

        An example dictionary looks like this:

            {
                u'name': u'johncosta+ttbot',
                u'laptop_version': None,
                u'laptop': u'linux',
                u'created': 1369698855.614588,
                u'userid': u'51a3f228aaa5cd45fe2669fb',
                u'registered': 1369698855.614588,
                u'acl': 0,
                u'fans': 1,
                u'points': 0,
                u'images':
                    {
                        u'fullfront': u'/roommanager_assets/avatars/8/fullfront.png',
                        u'headfront': u'/roommanager_assets/avatars/8/headfront.png'
                    },
                u'_id': u'51a3f228aaa5cd45fe2669fb',
                u'avatarid': 8,
                u'fanofs': 0
            }
        """
        for k, v in data.iteritems():
            self.__setattr__(k, v)
