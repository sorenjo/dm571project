#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, session, flash
from data import Users, Shows, Shifts
from datetime import datetime

app = Flask( __name__ )
app.secret_key = "secret" 
# login_manager = LoginManager()
# login_manager.init_app(app)

users = Users()
shows = Shows()
shifts = Shifts()

users.add( "admin", "admin", True )
shows.add( "test", datetime.now(), 120, 1 )

def render( file, **kwargs ):
    return render_template( file, user=users.get( session.get( "user" ) ), **kwargs )

@app.route( "/" )
def index():
    return render( "index.html" )

@app.route( "/create_show", methods = [ "POST", "GET" ] )
def create_show():
    global shows
    if request.method == "POST":
        title = request.form[ "nm" ]
        date_string = request.form[ "startdate" ]
        time_string = request.form[ "starttime" ]
        length_string = request.form[ "length" ]
        shifts_string = request.form[ "shifts" ]
        
        try:
            instant = datetime.strptime( f"{date_string}T{time_string}", "%Y-%m-%dT%H:%M" )
            length = int( length_string ) 
            shifts = int( shifts_string )
            shows.add( title, instant, length, shifts )

        except ValueError:
            flash( "Invalid data input" )
            return redirect( "/create_show" )

        return redirect( "/show_shows" )
    else: # request.method == "GET":
        return render( "create_show.html" )

@app.route( "/create_user", methods = [ "POST", "GET" ] )
def create_user():
    if request.method == "POST":
        uname = request.form[ "nm" ]
        pw = request.form[ "pw" ]
        is_super = "is_super" in request.form
        if uname not in users:
            users.add( uname, pw, is_super )
        else:
            pass # TODO error user already exists with that user name
        return redirect( "/" )
    else:
        return render( "create_user.html" )

@app.route( "/login", methods = [ "POST", "GET" ] )
def login():
    if request.method == "POST":
        name = request.form[ "nm" ]
        pw = request.form[ "pw" ]

        if users.login( name, pw ):
            session[ "user" ] = name
        return redirect( "/" )
    else:
        return render( "login.html" )

@app.route( "/logout" )
def logout():
    session[ "user" ] = None
    return redirect( "/" )

@app.route( "/my_shifts" )
def my_shifts():
    user_shifts = shifts.get( lambda x: x[0], session[ "user" ] ) 
    return render( "my_shifts.html", 
        th=[ "User", "Show id", "Time" ], 
        tr=map( # ( uid, sid ) -> ( uid, stitle, time )
            lambda x: ( x[0], ) + shows[ x[1] ].tuple()[:2], 
            user_shifts
        ),
        btn=map( # ( uid, sid ) -> ( href, link text )
            lambda x: ( f"/untake/{x[1]}", "Untake Shift" ),
            user_shifts
        )
    )

@app.route( "/untake/<show_id>" )
def untake( show_id ):
    shifts.untake( ( session[ "user" ], int( show_id ) ) )
    return redirect( "/my_shifts" )

@app.route( "/show_shows" )
def show_shows():
    return render( "show_shows.html", 
        th=[ "Title", "Time", "Length", "Shifts", "Show details" ], 
        tr=map( 
            lambda x: ( x.title, x.time, x.length, 
                f"{ len( shifts.get( lambda x: x[1], x.id ) ) } / { x.capacity }" ),
            shows.shows()
        ),
        btn=map(
            lambda x: ( f"/show_detail/{x.id}", x.title ),
            shows.shows()
        )
    )

@app.route( "/show_detail/<show_id>", methods = [ "POST" , "GET" ] )
def show_detail( show_id ):
    if request.method == "POST":
        shifts.take( session[ "user" ], int( show_id ) )
        return redirect( "/show_detail/{}".format( show_id ) )
    else:
        show = shows.get( int( show_id ) )
        return render( "show_detail.html", 
            th=["User"],
            tr=map( 
                lambda x: ( x[0], ),
                shifts.get( lambda x: x[1], int( show_id ) )
            ),
            show=show,
            disabled=len( shifts.get( lambda x: x[1], show.id ) ) == show.capacity or
            ( session[ "user" ], show.id ) in shifts
        )

if __name__ == "__main__":
    app.run( debug=True )
