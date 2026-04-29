"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern
"""


class TestGetActivities:
    """Test cases for retrieving activities"""

    def test_get_activities_returns_all_activities(self, client, test_activities):
        """
        ARRANGE: Set up test client and expected activities
        ACT: Make GET request to /activities
        ASSERT: Verify response includes all activities with expected fields
        """
        # ARRANGE
        expected_activity_count = len(test_activities)

        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_returns_correct_structure(self, client, test_activities):
        """
        ARRANGE: Define expected activity structure
        ACT: Fetch activities and inspect first activity
        ASSERT: Verify activity has all required fields
        """
        # ARRANGE
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # ACT
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]

        # ASSERT
        assert response.status_code == 200
        for field in required_fields:
            assert field in chess_club, f"Missing field: {field}"
        assert isinstance(chess_club["participants"], list)
        assert len(chess_club["participants"]) > 0

    def test_get_activities_includes_participant_count(self, client, test_activities):
        """
        ARRANGE: Set up known participant counts
        ACT: Get activities and check participant lists
        ASSERT: Verify participants match expected data
        """
        # ARRANGE
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # ACT
        response = client.get("/activities")
        data = response.json()

        # ASSERT
        assert response.status_code == 200
        assert data["Chess Club"]["participants"] == expected_chess_participants
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Gym Class"]["participants"]) == 2

    def test_get_activities_max_participants_field(self, client, test_activities):
        """
        ARRANGE: Know the max participants for Chess Club
        ACT: Fetch activities
        ASSERT: Verify max_participants is correctly returned
        """
        # ARRANGE
        chess_club_max = 12

        # ACT
        response = client.get("/activities")
        data = response.json()

        # ASSERT
        assert response.status_code == 200
        assert data["Chess Club"]["max_participants"] == chess_club_max
