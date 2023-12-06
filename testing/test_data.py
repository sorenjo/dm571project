#!/usr/bin/env python3
import unittest
from data import Data
from datetime import datetime

class TestUser( unittest.TestCase ):
    def test_add_user( self ):
        data = Data()
        data.add_user( "lars", "123", True )
        self.assertTrue( data.user_exists( "lars" ) )

    def test_add_show( self ):
        data = Data()
        sid = data.add_show( "testshow", datetime( 2023, 12, 8, hour=9 ), 90, 4)
        self.assertTrue( data.get_show( sid ) )

    def test_shift_table( self ):
        data = Data()
        data.add_user( "lars", "123", True )
        date = datetime( 2023, 12, 8, hour=9 )
        sid = data.add_show( "testshow", date, 90, 4)
        data.take( "lars", sid )
        tr, btn = data.shift_table( "lars" ) 
        self.assertTrue( [ *tr ] == [ ( "lars", "testshow", date ) ])
        self.assertTrue( [ *btn ] == [ ( f"/untake/{sid}", "Untake Shift" ) ])

    def test_shows_table( self ):
        data = Data()
        data.add_user( "lars", "123", True )
        date = datetime( 2023, 12, 8, hour=9 )
        sid = data.add_show( "testshow", date, 90, 4)
        data.take( "lars", sid )
        tr, btn = data.shows_table()
        self.assertTrue( [ *tr ] == [ ( "testshow", date, 90, "1 / 4" ) ] )

    def test_show_detail( self ):
        data = Data()
        data.add_user( "lars", "123", True )
        date = datetime( 2023, 12, 8, hour=9 )
        sid = data.add_show( "testshow", date, 90, 4)
        data.take( "lars", sid )
        tr, disabled = data.show_detail( sid, "lars" )
        self.assertTrue( [ *tr ] == [ ( "lars", ) ] )
        self.assertTrue( disabled )

    def test_login( self ):
        data = Data()
        data.add_user( "lars", "123", True )
        self.assertTrue( data.login( "lars", "123" ) )
        
