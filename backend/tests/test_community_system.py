from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app
from backend.models import CommunityAnswer, CommunityPost, UserXP, db
from backend.services.ai.assistant_service import mentor_assistant
from backend.services.community import create_answer, create_post, get_post_detail, get_or_create_user_xp, upvote_answer
from tests.test_support import SQLiteFixtureMixin


class TestCommunitySystem(SQLiteFixtureMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()
        cls.create_base_fixture()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            CommunityAnswer.query.filter_by(user_id=cls.fixture_ids["student_id"]).delete(synchronize_session=False)
            CommunityPost.query.filter_by(user_id=cls.fixture_ids["student_id"]).delete(synchronize_session=False)
            UserXP.query.filter_by(user_id=cls.fixture_ids["student_id"]).delete(synchronize_session=False)
            db.session.commit()
        cls.cleanup_fixture()

    def test_community_posting_and_xp_updates(self):
        with app.app_context():
            post = create_post(self.fixture_ids["student_id"], "How do I structure a Flask app?", "I want advice on organizing routes and services.")
            self.assertIsNotNone(post.id)

            answer = create_answer(post.id, self.fixture_ids["student_id"], "Use blueprints, services, and keep models separate.")
            self.assertIsNotNone(answer.id)
            self.assertGreaterEqual(get_or_create_user_xp(self.fixture_ids["student_id"]).xp_points, 15)

            voted = upvote_answer(answer.id)
            self.assertEqual(voted.votes, 1)
            self.assertGreaterEqual(get_or_create_user_xp(self.fixture_ids["student_id"]).xp_points, 20)

            detail = get_post_detail(post.id)
            self.assertEqual(detail["post"].id, post.id)
            self.assertTrue(detail["answers"])

            mentor_payload = mentor_assistant(self.fixture_ids["student_id"], "Show community questions")
            self.assertEqual(mentor_payload["intent"], "community_help")
            self.assertIn("/community", mentor_payload["answer"])

    def test_community_routes_render(self):
        self.login_student(self.client)
        self.assertEqual(self.client.get("/community").status_code, 200)
        self.assertEqual(self.client.get("/community/post").status_code, 200)

        post_response = self.client.post(
            "/community/post",
            data={"title": "Best way to practice algorithms?", "content": "Share your routine for coding interviews."},
            follow_redirects=False,
        )
        self.assertIn(post_response.status_code, [302, 303])
        location = post_response.headers.get("Location", "")
        self.assertIn("/community/question/", location)
        question_response = self.client.get(location)
        self.assertEqual(question_response.status_code, 200)

        with app.app_context():
            post = CommunityPost.query.filter_by(title="Best way to practice algorithms?").order_by(CommunityPost.id.desc()).first()
            self.assertIsNotNone(post)

        answer_response = self.client.post(
            "/community/answer",
            data={"post_id": post.id, "answer_text": "Practice a few problems daily and review edge cases."},
            follow_redirects=True,
        )
        self.assertEqual(answer_response.status_code, 200)
        self.assertIn(b"Votes", answer_response.data)


if __name__ == "__main__":
    unittest.main()

