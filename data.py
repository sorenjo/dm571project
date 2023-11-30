#!/bin/env/python3
class Data:
    _instance = None

    def __new__( cls ):
        if not cls._instance:
            cls._instance = super( Data, cls ).__new__( cls )
        return cls._instance

    def __init__( self ):
        self._users = dict()
        self._shows = dict() 
        self._shifts = []
        self.show_id_counter = 0

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

    class Show:

        def __init__( self, title, instant, length, cap, id ):
            self.title = title
            self.time = instant
            self.length = length
            self.id = id
            self.capacity = cap

        def tuple( self ):
            return self.title, self.time, self.length, self.capacity, self.id
        
        def __str__( self ):
            return "\"" +  self.title + "\" " + str( self.time )

        def __repr__( self ):
            return self.title

    # adds given user.
    # precondition: there does not already exist a user with the given username
    """
    >>> data = Data()
    >>> data.add_user( "lars", "asdf", False )
    >>> data.user_exists( "lars" )
    True
    """
    def add_user( self, name, password, is_super ):
        self._users[ name ] = self.User( name, password, is_super )

    # determines if the provided username/password combination yields a valid user login
    def login( self, uname, password ):
        u = self._users.get( uname )
        return u and u.password == password 

    #get_user = Data._users.get
    def get_user( self, user ):
        return self._users.get( user )

    def user_exists( self, username ):
        return username in self._users

    def shift_table( self, username ):
        shifts = self.get_shifts_by_user( username )
        return map( # ( uid, sid ) -> ( uid, stitle, time )
            lambda x: ( x[0], self._shows[ x[1] ].title, self._shows[ x[1] ].time ),
            shifts
        ), map( # ( uid, sid ) -> ( href, link text )
            lambda x: ( f"/untake/{x[1]}", "Untake Shift" ),
            shifts
        )
    
    def get_shifts_by_show( self, show_id ):
        return self.get_shift( lambda x: x[1], show_id )
        
    def get_shifts_by_user( self, user ):
        return self.get_shift( lambda x: x[0], user )

    # untake = _shifts.remove
    def untake( self, shift ):
        return  self._shifts.remove( shift )

    def add_show( self, title, instant, length, cap ):
        id = self.next_show_id()
        show = self.Show( title, instant, length, cap, id )
        self._shows[ show.id ] = show
    
    def next_show_id( self ):
            self.show_id_counter += 1
            return self.show_id_counter

    def get_show( self, show_id ):
        return self._shows.get( show_id )
        
    # shows = _shows.values 
    def shows( self ):
        return self._shows.values()

    def shows_table( self ):
        shows = self._shows.values()
        return map( 
            lambda x: ( x.title, x.time, x.length, 
                f"{ len( self.get_shifts_by_show( x.id ) ) } / { x.capacity }" ),
            shows
        ), map(
            lambda x: ( f"/show_detail/{x.id}", x.title ),
            shows
        )
    
    def show_detail( self, show_id, user ):
        show = self._shows.get( show_id )
        return map( 
                lambda x: ( x[0], ),
                self.get_shifts_by_show( int( show_id ) )
        ), len( self.get_shifts_by_show( show.id ) ) == show.capacity or ( user, show.id ) in self._shifts

    def take( self, uid, sid ):
        self._shifts.append( ( uid, sid ) )

    def get_shift( self, key, id ):
        return [ s for s in self._shifts if key( s ) == id ]
if __name__ == "__main__":
    import doctest
    doctest.testmod()

