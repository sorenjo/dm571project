class Users:
    users = dict()

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
        self.users[ name ] = self.User( name, password, is_super )

    # determines if the provided username/password combination yields a valid user login
    def login( self, uname, password ):
        u = self.users.get( uname )
        return True if u and u.password == password else False

    __contains__ = users.__contains__
    __getitem__ = users.__getitem__
    get = users.get

class Shows:
    shows = []
    def __init( self ):
        pass
        
    class Show:
        id_counter = 0
        def __init__( self, title, instant ):
            self.title = title
            self.time = instant

        def next_id():
            Show.id_counter += 1
            return Show.id_counter

        def take_shift( self, user ):
            self.shifts.append( user )
        
        def tuple( self ):
            return ( self.title, self.time )
        
        def __str__( self ):
            return "\"" +  self.title + "\" " + str( self.time )

        def __repr__( self ):
            return str( self )

    def add( self, title, instant ):
        self.shows.append( self.Show( title, instant ) )

    __contains__ = shows.__contains__
    __getitem__ = shows.__getitem__


    
