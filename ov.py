#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, session, flash
from data import Data
from datetime import datetime

app = Flask( __name__ )
app.secret_key = "secret" 

# users.add( "admin", "admin", True )
# shows.add( "test", datetime.now(), 120, 3 )

data = Data()

data.add_user( "admin", "admin", True )
data.add_show( "test", datetime.now(), 120, 3 )

def render( file, **kwargs ):
    return render_template( file, user=data.get_user( session.get( "user" ) ), **kwargs )

@app.route( "/" )
def index():
    return render( "index.html" )

@app.route( "/create_show", methods = [ "POST", "GET" ] )
def create_show():
    if request.method == "GET":
        return render( "create_show.html" )

    # else request.method == "POST":
    title = request.form[ "nm" ]
    date_string = request.form[ "startdate" ]
    time_string = request.form[ "starttime" ]
    length_string = request.form[ "length" ]
    shifts_string = request.form[ "shifts" ]
    
    try:
        instant = datetime.strptime( f"{date_string}T{time_string}", "%Y-%m-%dT%H:%M" )
        length = int( length_string ) 
        shifts = int( shifts_string )
        data.add_show( title, instant, length, shifts )

    except ValueError:
        flash( "Invalid data input" )
        return redirect( "/create_show" )

    return redirect( "/show_shows" )

@app.route( "/create_user", methods = [ "POST", "GET" ] )
def create_user():
    if request.method == "GET":
        return render( "create_user.html" )
    
    # else request.method == "POST":
    uname = request.form[ "nm" ]
    pw = request.form[ "pw" ]
    is_super = "is_super" in request.form
    if not data.user_exists( uname ):
        data.add_user( uname, pw, is_super )
    else:
        pass # TODO error user already exists with that user name
    return redirect( "/" )

@app.route( "/login", methods = [ "POST", "GET" ] )
def login():
    if request.method == "GET":
        return render( "login.html" )

    # else request.method == "POST":
    name = request.form[ "nm" ]
    pw = request.form[ "pw" ]

    if data.login( name, pw ):
        session[ "user" ] = name
    return redirect( "/" )

@app.route( "/logout" )
def logout():
    session[ "user" ] = None
    return redirect( "/" )

@app.route( "/my_shifts" )
def my_shifts():
    tr, btn = data.shift_table( session[ "user" ] )
    return render( "my_shifts.html", 
        th=[ "User", "Show id", "Time" ], 
        tr=tr,
        btn=btn
    )

@app.route( "/untake/<show_id>" )
def untake( show_id ):
    data.untake( ( session[ "user" ], int( show_id ) ) )
    return redirect( "/my_shifts" )

@app.route( "/show_shows" )
def show_shows():
    tr, btn = data.shows_table()
    return render( "show_shows.html", 
        th=[ "Title", "Time", "Length", "Shifts", "Show details" ], 
        tr=tr,
        btn=btn
    )

@app.route( "/show_detail/<show_id>", methods = [ "POST" , "GET" ] )
def show_detail( show_id ):
    if request.method == "GET":
        tr, disabled = data.show_detail( int( show_id ), session[ "user" ] )
        return render( "show_detail.html", 
            th=[ "User" ],
            tr=tr,
            show=data.get_show( int( show_id ) ),
            disabled=disabled
        )

    # else request.method == "POST":
    data.take( session[ "user" ], int( show_id ) )
    return redirect( "/show_detail/{}".format( show_id ) )

if __name__ == "__main__":
    app.run( debug=True )
