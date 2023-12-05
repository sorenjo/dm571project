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

    def test_add_show( self ):
        pass

    def test_show_detail( self ):
        pass

    def test_untake( self ):
        pass
