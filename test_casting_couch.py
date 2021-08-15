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
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY3VHhXcTZCVDA1RV9hZzdFTC1NWiJ9.eyJpc3MiOiJodHRwczovL2VjY3dlaXpoaS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE4NThiMzhiNzJmNzAwNmFlNmNhZmMiLCJhdWQiOiJteUZvb2JhciIsImlhdCI6MTYyODk4NzA1MiwiZXhwIjoxNjI4OTk0MjUyLCJhenAiOiJQdGdLN1FoYnVkdGYxWlVXbklOSGxiV3BhS0NwZ3JxVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.xGMFvGhllihBwUvlIxqJAz9lqK2WiJOKuXLx35TMKpvZiVaPFDGuzcsdGbvf-9pnni3rR4yNF2u-pPmXofMd17tPKYgiQFCwjX3xusKZAL_tWKtdGekIVxgMV6wGyC4pzb6Rj86PwwqGqXgyhDLafRZIjxLsxMNL3IkEXiL9km_LOW2ogA0tj86hAQaiz7BmO4KJTPKOB1lF3Zidvb72weEUDzTQTayHNgbH8zXGgFUgv6kMHwqCbgo7YaVg512QgsO_PiTOjmdw1QI0nQE-kfSfe2nj0ZcoIPWj5R4IraEM8ickQGx6vE6OA3H7pUQOKRxDajKwG4KKfINpsSCOmQ"
}
CASTING_DIRECTOR_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY3VHhXcTZCVDA1RV9hZzdFTC1NWiJ9.eyJpc3MiOiJodHRwczovL2VjY3dlaXpoaS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE4NTkxZTgxZDk5YjAwNzBlZjZlMjciLCJhdWQiOiJteUZvb2JhciIsImlhdCI6MTYyODk4NzExNiwiZXhwIjoxNjI4OTk0MzE2LCJhenAiOiJQdGdLN1FoYnVkdGYxWlVXbklOSGxiV3BhS0NwZ3JxVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.o1hK4wZ-A8tMqYiTlKtv_ykc73sB2fg-W0blls3aoCiwfSvB5QZm1PxicPB7BE4dKztadR84BkkTGm3JOKzl74aGrEHYgzyfn1Qp5MVg485efoNudiq7kwtmaoAlAv9NCehmY_-Tst1CUahAuwhFkSnFBZUPgfAtQ4wkRBt2DyGavgYnR6tG3mW94KSESTwkh3Cc6xwCOg6VjjKauX-G8MQYkyr6wF8BfhgHNasrGIOEr-bZEA_Q9CKMJvRSGDnD_P7vQ_cpTUPJwzTxHbwrI71QcPgyzdoc0fuWjW4UWvcZX6c7qEFlM-jJRu10c0YDw8VnTjgd7r3Z5uelbY3tJw"
}
EXECUTIVE_PRODUCER_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY3VHhXcTZCVDA1RV9hZzdFTC1NWiJ9.eyJpc3MiOiJodHRwczovL2VjY3dlaXpoaS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTE4NTkzZGYwZDEzMTAwNzFmZjQ2NjYiLCJhdWQiOiJteUZvb2JhciIsImlhdCI6MTYyODk4NzE2MiwiZXhwIjoxNjI4OTk0MzYyLCJhenAiOiJQdGdLN1FoYnVkdGYxWlVXbklOSGxiV3BhS0NwZ3JxVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.DepvR3YJkkG8tIXuJAsONQypJAz26qk6dkuL9vMRzYUnkqrCcaziUqgrIT8bDNesmz_J2g9k4NJ7eRB1N2RHI69y59bvJhyw4qvZethEYo8XJgAuAXUcAucNkbaczN5U5HLGSj7gcbGvEanKIOUSrXRHIVL9ct6l85amHwPb2juA2M5GwOOYbdHt0DJYmNt0Qqv1SmdCzwLN-Jo68RjQcFqOqyHDLGyiO1JnopFkpMoVGVpdfeP2QnB1erqRIFHbwLba1Qv_TZlfleceJyi03MFsWRY6HyCD5bqDZyyPjBHI1KotSCXC4DmgqYpARIDl0abIzd4BcQox7LY9okm50g"
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

    def test_add_actors_success(self):
        res = self.client().post('/actors', json={
            "name": "Charlie",
            "age": 45,
            "gender": "F"
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_missing_field_add_actors_fail(self):
        res = self.client().post('/actors', json={
            "age": 45,
            "gender": "F"
        }, headers=CASTING_DIRECTOR_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
