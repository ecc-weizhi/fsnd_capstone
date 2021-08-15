import json
import unittest
from datetime import datetime

from app import create_app
from models import setup_db, db
from models.actor import Actor
from models.movie import Movie

TEST_DB_PATH = "postgresql://weizhi:test1234@localhost:5432/castingcouch_test"

CASTING_ASSISTANT_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY3VHhXcTZCVDA1RV9hZzdFTC1NWiJ9.eyJpc3MiOiJodHRwczovL2VjY3dlaXpoaS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE4NThiMzhiNzJmNzAwNmFlNmNhZmMiLCJhdWQiOiJteUZvb2JhciIsImlhdCI6MTYyOTAxMjI5OCwiZXhwIjoxNjI5MDE5NDk4LCJhenAiOiJQdGdLN1FoYnVkdGYxWlVXbklOSGxiV3BhS0NwZ3JxVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.sBd9f4qT9BjI93hUt-yUVRI9cWQ3UgR_HRpJAhXKih_JUHg4w42i7T-mCZM6XRb1yH3duTWwaatAFQOeRTofQ8SmkIlnnOEZHJUCAXg-gnHHq_zV4AX8q8hkhH7ZinIQkaQ5xuXxbXweODdcpS7n0y8DysbJpaf7K524OzOb0Gt4wPSK5qk0kmfC-vfUJWKdVM4zoml4Sj0dAKoHEH_h6L4Q2VBK2RvyspNVAtHk9x51ySRYhRFFzEJOxUuDmgDjrqSmYWKBqPsCubi8EYTcXi2iK7nafWpvel9CJWIqCYT0zXWgtlilLE8brk486-7SwHfCeBnr9XABu07hLH1iTg"
}
CASTING_DIRECTOR_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY3VHhXcTZCVDA1RV9hZzdFTC1NWiJ9.eyJpc3MiOiJodHRwczovL2VjY3dlaXpoaS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE4NTkxZTgxZDk5YjAwNzBlZjZlMjciLCJhdWQiOiJteUZvb2JhciIsImlhdCI6MTYyOTAxMjIwMSwiZXhwIjoxNjI5MDE5NDAxLCJhenAiOiJQdGdLN1FoYnVkdGYxWlVXbklOSGxiV3BhS0NwZ3JxVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.HLyrmGxAFsS5pqf_t1KmLRMF7WBPC6Qlp2zJZn_5s0gI2RFa_pFUMDJFwg0mGTFqA3UbIrivp_S_rrG68eylQPyAaoZRHewKpkIYNbvEKcDp5StLmF4AZVz9O3OqaZPSy0UDJTkHaOPnHhDh4AQ0CTQ-ju20AF9TdvkU1TqQ8L2_c80hkOqyzQho1Knc0jX0j_hc4AoDX7qY5JtaLI7gPS-aAl_LXxjTfkRMmQnFq0uqp328D_FKwPQmp5GUjRSwf_ssL2UgxVXGN9uReFDtkRXOlghAjLRX_-pzzOHiaLpdMH6BUFU-60d7rtILazoUyCLfgD94efk7cUbgOxqMkg"
}
EXECUTIVE_PRODUCER_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY3VHhXcTZCVDA1RV9hZzdFTC1NWiJ9.eyJpc3MiOiJodHRwczovL2VjY3dlaXpoaS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE4NTkzZGYwZDEzMTAwNzFmZjQ2NjYiLCJhdWQiOiJteUZvb2JhciIsImlhdCI6MTYyOTAxMTk0NSwiZXhwIjoxNjI5MDE5MTQ1LCJhenAiOiJQdGdLN1FoYnVkdGYxWlVXbklOSGxiV3BhS0NwZ3JxVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.Ne02peqOaKowxYg7n82OL4PdxCy6pxXM5unt62fplvIfg7DIdE233CxhFlBLdBqtXEd_L4yswiiJ2n0ilCY2ACxsZ8ST_g8EoTt6FqEXw-5WhjHKQU2IGGxzLWtgU2UW2nOtJW-Skufgdj7kvxZGBxxfL5DvpqCJhlGBITQO3d02tlN4O1KikZ5Q3zCq-J0OlR-I59FaZhCx1J0su-bfBY_Vq1zJagNR3p7_GtDMihGZxJEPPbqIu9J-U5QtXR5esM6eWm8YbhEkX3NRn7KSyPr4eQwFWb0XoQblvFEi9LFQCbYTgiFZ0TkZ68sKWgHFQgEgJ4r3bkwg7yK-pJv0Tw"
}


class CastingCouchTestCase(unittest.TestCase):
    database_path = "postgresql://weizhi:test1234@localhost:5432/castingcouch_test"

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, TEST_DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            self._initialize_db()

    def _initialize_db(self):
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
        res = self.client().get('/actors', headers=CASTING_ASSISTANT_HEADERS)
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
        res = self.client().delete('/actors/1', headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 1)

    def test_id_not_exist_delete_actor_fail(self):
        res = self.client().delete('/actors/10', headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_actor_success(self):
        res = self.client().post('/actors', json={
            "name": "Charlie",
            "age": 45,
            "gender": "F"
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_missing_field_add_actor_fail(self):
        res = self.client().post('/actors', json={
            "age": 45,
            "gender": "F"
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_actor_success(self):
        res = self.client().patch('/actors/1', json={
            "name": "Ahmad",
            "age": 50,
            "gender": "F"
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_id_not_exist_patch_actor_fail(self):
        res = self.client().patch('/actors/10', json={
            "name": "Ahmad",
            "age": 50,
            "gender": "F"
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=CASTING_ASSISTANT_HEADERS)
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
        res = self.client().delete('/movies/1', headers=EXECUTIVE_PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 1)

    def test_id_not_exist_delete_movie_fail(self):
        res = self.client().delete('/movies/10', headers=EXECUTIVE_PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_movie_success(self):
        res = self.client().post('/movies', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=EXECUTIVE_PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_missing_field_add_movie_fail(self):
        res = self.client().post('/movies', json={
            "release_date": datetime.utcnow(),
        }, headers=EXECUTIVE_PRODUCER_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_movie_success(self):
        res = self.client().patch('/movies/1', json={
            "title": "Harry Potter",
            "release_date": datetime.utcnow(),
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_id_not_exist_patch_movie_fail(self):
        res = self.client().patch('/movies/10', json={
            "title": "Inception",
            "release_date": datetime.utcnow(),
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
