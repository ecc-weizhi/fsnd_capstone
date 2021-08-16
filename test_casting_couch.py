import json
import os
import unittest
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app import create_app
from models import setup_db, db
from models.actor import Actor
from models.movie import Movie

TEST_DB_PATH = "postgresql://weizhi:test1234@localhost:5432/castingcouch_test"
CASTING_ASSISTANT_USERNAME = os.environ.get("CASTING_ASSISTANT_USERNAME", None)
CASTING_ASSISTANT_PASSWORD = os.environ.get("TEST_ACCOUNT_PASSWORD", None)
CASTING_DIRECTOR_USERNAME = os.environ.get("CASTING_DIRECTOR_USERNAME", None)
CASTING_DIRECTOR_PASSWORD = os.environ.get("TEST_ACCOUNT_PASSWORD", None)
EXECUTIVE_PRODUCER_USERNAME = os.environ.get("EXECUTIVE_PRODUCER_USERNAME", None)
EXECUTIVE_PRODUCER_PASSWORD = os.environ.get("TEST_ACCOUNT_PASSWORD", None)
CLIENT_ID = os.environ.get("CLIENT_ID", None)
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)


class CastingCouchTestCase(unittest.TestCase):
    _database_path = "postgresql://weizhi:test1234@localhost:5432/castingcouch_test"
    _casting_assistant_headers = None
    _casting_director_headers = None
    _executive_producer_headers = None

    @classmethod
    def setUpClass(cls):
        url = "https://eccweizhi-fsnd.us.auth0.com/oauth/token"
        post_fields = {
            "grant_type": "password",
            "audience": "myFoobar",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        # casting assistant
        post_fields["username"] = CASTING_ASSISTANT_USERNAME
        post_fields["password"] = CASTING_ASSISTANT_PASSWORD
        request = Request(url, urlencode(post_fields).encode())
        response = urlopen(request).read()
        data = json.loads(response)
        cls._casting_assistant_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['access_token']}"
        }

        # casting director
        post_fields["username"] = CASTING_DIRECTOR_USERNAME
        post_fields["password"] = CASTING_DIRECTOR_PASSWORD
        request = Request(url, urlencode(post_fields).encode())
        response = urlopen(request).read()
        data = json.loads(response)
        cls._casting_director_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['access_token']}"
        }

        # executive producer
        post_fields["username"] = EXECUTIVE_PRODUCER_USERNAME
        post_fields["password"] = EXECUTIVE_PRODUCER_PASSWORD
        request = Request(url, urlencode(post_fields).encode())
        response = urlopen(request).read()
        data = json.loads(response)
        cls._executive_producer_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {data['access_token']}"
        }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, TEST_DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            self._populate_db()

    def _populate_db(self):
        self._insert_actor("Ash", "25", "M")
        self._insert_actor("Bob", "35", "F")
        self._insert_movie("Hobbit", datetime.utcnow())
        self._insert_movie("Avengers", datetime.utcnow())

    def _insert_actor(self, name, age, gender):
        actor = Actor(name, age, gender)
        db.session.add(actor)
        db.session.commit()

    def _insert_movie(self, title, release_date):
        movie = Movie(title, release_date)
        db.session.add(movie)
        db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, TEST_DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.drop_all()

    def test_get_actors_success(self):
        res = self.client().get('/actors', headers=self._casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertEqual(len(data['actors']), 2)

    def test_no_permission_get_actors_fail(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_actor_success(self):
        res = self.client().delete('/actors/1', headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 1)

    def test_id_not_exist_delete_actor_fail(self):
        res = self.client().delete('/actors/10', headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_actor_success(self):
        res = self.client().post('/actors', json={
            "name": "Charlie",
            "age": 45,
            "gender": "F"
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_missing_field_add_actor_fail(self):
        res = self.client().post('/actors', json={
            "age": 45,
            "gender": "F"
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_actor_success(self):
        res = self.client().patch('/actors/1', json={
            "name": "Ahmad",
            "age": 50,
            "gender": "F"
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_id_not_exist_patch_actor_fail(self):
        res = self.client().patch('/actors/10', json={
            "name": "Ahmad",
            "age": 50,
            "gender": "F"
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=self._casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertEqual(len(data['movies']), 2)

    def test_no_permission_get_movies_fail(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_movie_success(self):
        res = self.client().delete('/movies/1', headers=self._executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 1)

    def test_id_not_exist_delete_movie_fail(self):
        res = self.client().delete('/movies/10', headers=self._executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_movie_success(self):
        res = self.client().post('/movies', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=self._executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_missing_field_add_movie_fail(self):
        res = self.client().post('/movies', json={
            "release_date": datetime.utcnow(),
        }, headers=self._executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_movie_success(self):
        res = self.client().patch('/movies/1', json={
            "title": "Harry Potter",
            "release_date": datetime.utcnow(),
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_id_not_exist_patch_movie_fail(self):
        res = self.client().patch('/movies/10', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_casting_assistant_can_get_movies(self):
        res = self.client().get('/movies', headers=self._casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertEqual(len(data['movies']), 2)

    def test_casting_assistant_cannot_add_movie(self):
        res = self.client().post('/movies', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=self._casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_casting_director_can_add_actor(self):
        res = self.client().post('/actors', json={
            "name": "Charlie",
            "age": 45,
            "gender": "F"
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_casting_director_cannot_add_movie(self):
        res = self.client().post('/movies', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=self._casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_executive_producer_can_add_movie(self):
        res = self.client().post('/movies', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=self._executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_executive_producer_can_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self._executive_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
