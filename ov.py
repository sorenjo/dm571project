#!/usr/bin/env python3
from flask import Flask
from flask import render_template, request, redirect
# from flask_login import LoginManager
import datetime

app = Flask( __name__ )
app.secret_key = "secret" 
# login_manager = LoginManager()
# login_manager.init_app(app)

shows = []
users = dict()

class Show:
    def __init__( self, title, instant ):
        self.title = title
        self.time = instant
        self.shifts = []

    def take_shift( user ):
        self.shifts.append( user )
    
    def __str__( self ):
        return "\"" +  self.title + "\" " + str( self.time )

    def __repr__( self ):
        return str( self )

class User:
    next_id = 0
    def __init__( self, name, password, is_super ):
        self.name = name
        self.password = password 
        self.shifts = []
        self.is_super = is_super
        self.id = next_id
        next_id += 1

    def list_shifts( self ):
        global shows
        l = []
        for show in shows:
            if self in show.shifts: 
                l.append( show )
        return l
    

@app.route( "/" )
def index():
    return render_template( "index.html", shows=shows)

@app.route( "/create_show", methods = [ "POST", "GET" ] )
def create_show():
    global shows
    if request.method == "POST":
        title = request.form[ "nm" ]
        shows.append( Show( title, datetime.datetime.now() ) )
        print( shows )
        return redirect( "/" )
    else:
        return render_template( "create_show.html" )

@app.route( "/create_user", methods = [ "POST", "GET" ] )
def create_user():
    if request.method == "POST":
        name = request.form[ "nm" ]
        pw = request.form[ "pw" ]
        users.add( name, User( name, pw ) )
        return redirect( "/" )
    else:
        return render_template( "create_user.html" )

@app.route( "/login", methods = [ "POST", "GET" ] )
def login():
    if request.method == "POST":
        name = request.form[ "nm" ]
        pw = request.form[ "pw" ]
        if name in users: # if user exists
            session[ "id" ] = users[ name ].id
        return redirect( "/" )
    else:
        return render_template( "login.html" )

if __name__ == "__main__":
    app.run( debug=True )
