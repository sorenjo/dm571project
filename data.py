class Users:
    _users = dict()

    def __init__( self ):
        pass

    class User:
        def __init__( self, name, password, is_super ):
            self.uname = name
            self.password = password 
            self.shifts = []
            self.is_super = is_super

        def list_shifts( self ):
            global shows
            l = []
            for show in shows:
                if self in show.shifts: 
                    l.append( show )
            return l

        def __eq__( self, other ):
            if type( other ) is str:
                return self.uname == other

    # adds given user.
    # precondition: there does not already exist a user with the given username
    def add( self, name, password, is_super ):
        self._users[ name ] = self.User( name, password, is_super )

    # determines if the provided username/password combination yields a valid user login
    def login( self, uname, password ):
        u = self._users.get( uname )
        return True if u and u.password == password else False

    # med alle de her funktionsaliaser er det måske en idé bare at inherite fra dict
    __contains__ = _users.__contains__
    __getitem__ = _users.__getitem__
    get = _users.get

class Shows:
    _shows = dict() 
    id_counter = 0
    def __init( self ):
        pass
        
    class Show:

        def __init__( self, title, instant ):
            self.title = title
            self.time = instant
            self.id = self.next_id()

        def tuple( self ):
            return self.title, self.time

        @staticmethod
        def next_id():
            Shows.id_counter += 1
            return Shows.id_counter

        
        def __str__( self ):
            return "\"" +  self.title + "\" " + str( self.time )

        def __repr__( self ):
            return self.title

    def add( self, title, instant ):
        show = self.Show( title, instant )
        self._shows[ show.id ] = show


    # med alle de her funktionsaliaser er det måske en idé bare at inherite fra dict
    __contains__ = _shows.__contains__
    __getitem__ = _shows.__getitem__
    __repr__ = _shows.__repr__
    shows = _shows.values
    get = _shows.get


# TODO er der nogle måder det her kan gøres så det er med static variable og static metoder, så det bliver lidt en singletonclass?
class Shifts:
    _shifts = []
    def __init__( self ):
        pass

    def take( self, uid, sid ):
        self._shifts.append( ( uid, sid ) )

    def get( self, key, id ):
        return [ s for s in self._shifts if key( s ) == id ]
