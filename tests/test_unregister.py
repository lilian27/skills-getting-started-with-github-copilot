"""
Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern
"""


class TestUnregister:
    """Test cases for student unregistration"""

    def test_unregister_success_removes_student(self, client, test_activities):
        """
        ARRANGE: Select student already registered for activity
        ACT: Send unregister request
        ASSERT: Verify student is removed from participants
        """
        # ARRANGE
        email_to_remove = "michael@mergington.edu"
        activity = "Chess Club"
        initial_count = len(test_activities[activity]["participants"])
        assert email_to_remove in test_activities[activity]["participants"]

        # ACT
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )

        # ASSERT
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email_to_remove} from {activity}"
        assert email_to_remove not in test_activities[activity]["participants"]
        assert len(test_activities[activity]["participants"]) == initial_count - 1

    def test_unregister_different_activities(self, client, test_activities):
        """
        ARRANGE: Select participants from different activities
        ACT: Unregister from Programming Class
        ASSERT: Verify removal works across different activities
        """
        # ARRANGE
        email_to_remove = "emma@mergington.edu"
        activity = "Programming Class"

        # ACT
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )

        # ASSERT
        assert response.status_code == 200
        assert email_to_remove not in test_activities[activity]["participants"]

    def test_unregister_student_not_found(self, client, test_activities):
        """
        ARRANGE: Use email not registered for activity
        ACT: Send unregister request for non-participant
        ASSERT: Verify request fails with 400 status
        """
        # ARRANGE
        non_participant_email = "nonexistent@mergington.edu"
        activity = "Chess Club"

        # ACT
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": non_participant_email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_activity_not_found(self, client, test_activities):
        """
        ARRANGE: Use non-existent activity name
        ACT: Send unregister request for invalid activity
        ASSERT: Verify request fails with 404 status
        """
        # ARRANGE
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"

        # ACT
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_unregister_preserves_other_participants(self, client, test_activities):
        """
        ARRANGE: Get all current participants
        ACT: Remove one participant
        ASSERT: Verify other participants remain intact
        """
        # ARRANGE
        email_to_remove = "michael@mergington.edu"
        activity = "Chess Club"
        other_participants = [
            p for p in test_activities[activity]["participants"] 
            if p != email_to_remove
        ]

        # ACT
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )

        # ASSERT
        assert response.status_code == 200
        for remaining_email in other_participants:
            assert remaining_email in test_activities[activity]["participants"]

    def test_unregister_duplicate_attempt_fails(self, client, test_activities):
        """
        ARRANGE: Unregister a student once
        ACT: Attempt to unregister same student again
        ASSERT: Verify second attempt fails
        """
        # ARRANGE
        email_to_remove = "daniel@mergington.edu"
        activity = "Chess Club"

        # ACT - First unregister (should succeed)
        response1 = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )
        # ACT - Second unregister (should fail)
        response2 = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )

        # ASSERT
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]
