#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, session
from data import Users, Shows, Shifts
import datetime

app = Flask( __name__ )
app.secret_key = "secret" 
# login_manager = LoginManager()
# login_manager.init_app(app)

users = Users()
shows = Shows()
shifts = Shifts()

users.add( "admin", "admin", True )

class Shifts:
    shifts = []
    
    def insert(show, user):
        Shifts.shifts.append((show, user))

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
        shows.add( title, datetime.datetime.now() )
        print( shows )
        return redirect( "/" )
    else:
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
    return render( "my_shifts.html" )

@app.route( "/show_shows" )
def show_shows():
    return render( "show_shows.html", th=["Title", "Time", "Shifts"], tr=[ s.tuple() for s in shows.shows() ] )

#TODO method not allowed når man forsøger take shift
@app.route( "/show_detail/<show_id>" )
def show_detail( show_id, methods = [ "POST", "GET" ] ):
    if request.method == "POST":
        shifts.take( session[ "user" ], show_id )
        redirect( "/show_detail/{}".format( show_id ) )
    else:
        return render( "show_detail.html", show=shows.get( int( show_id ) ) )

if __name__ == "__main__":
    app.run( debug=True )
