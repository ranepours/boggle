from unittest import TestCase
from app import app
from flask import session


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        """display html, check session"""
        with self.client:
            res = self.client.get('/')
            self.assertIn(b'High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Seconds Left:', res.data)

            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))


    def test_word_valid(self):
        """test word validity"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["A", "B", "C", "D", "E"], 
                                 ["F", "G", "H", "I", "J"], 
                                 ["K", "L", "M", "N", "O"], 
                                 ["L", "P", "P", "Q", "R"], 
                                 ["O", "O", "S", "T", "U"]]
        response = self.client.get('/check-word?word=loop')
        self.assertEqual(response.json['result'], 'ok')

    def test_exist(self):
        """test if word is in dictionary"""
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_showing(self):
        """test if word on board"""
        self.client.get('/')
        response = self.client.get(
            '/check-word?word=njostfacweolrpd')
        self.assertEqual(response.json['result'], 'not-word')
