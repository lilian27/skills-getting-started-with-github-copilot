"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern
"""


class TestSignup:
    """Test cases for student signup"""

    def test_signup_success_new_student(self, client, test_activities):
        """
        ARRANGE: Prepare new student email and target activity
        ACT: Send signup request
        ASSERT: Verify student is added and response is correct
        """
        # ARRANGE
        new_email = "newstudent@mergington.edu"
        activity = "Chess Club"
        initial_participants = len(test_activities[activity]["participants"])

        # ACT
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity}"
        assert new_email in test_activities[activity]["participants"]
        assert len(test_activities[activity]["participants"]) == initial_participants + 1

    def test_signup_different_activities(self, client, test_activities):
        """
        ARRANGE: Prepare signup for different activity
        ACT: Sign up for Programming Class
        ASSERT: Verify signup works for any valid activity
        """
        # ARRANGE
        new_email = "alex@mergington.edu"
        activity = "Programming Class"

        # ACT
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response.status_code == 200
        assert new_email in test_activities[activity]["participants"]

    def test_signup_duplicate_email_fails(self, client, test_activities):
        """
        ARRANGE: Use email already registered for activity
        ACT: Send signup request with duplicate email
        ASSERT: Verify request fails with 400 status
        """
        # ARRANGE
        duplicate_email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # ACT
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": duplicate_email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found(self, client, test_activities):
        """
        ARRANGE: Use non-existent activity name
        ACT: Send signup request for invalid activity
        ASSERT: Verify request fails with 404 status
        """
        # ARRANGE
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"

        # ACT
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_same_student_different_activities(self, client, test_activities):
        """
        ARRANGE: Use same email for two different activities
        ACT: Sign up for Chess Club then Programming Class
        ASSERT: Verify student can join multiple activities
        """
        # ARRANGE
        new_email = "versatile@mergington.edu"

        # ACT
        response1 = client.post(
            f"/activities/Chess Club/signup",
            params={"email": new_email}
        )
        response2 = client.post(
            f"/activities/Programming Class/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert new_email in test_activities["Chess Club"]["participants"]
        assert new_email in test_activities["Programming Class"]["participants"]

    def test_signup_preserves_other_participants(self, client, test_activities):
        """
        ARRANGE: Get current participants count
        ACT: Add new participant
        ASSERT: Verify original participants are still there
        """
        # ARRANGE
        chess_club_original_participants = test_activities["Chess Club"]["participants"].copy()
        new_email = "newmember@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/Chess Club/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response.status_code == 200
        for original_email in chess_club_original_participants:
            assert original_email in test_activities["Chess Club"]["participants"]
