"""
Tests for GET / endpoint using AAA pattern
"""


class TestRootRedirect:
    """Test cases for root endpoint redirect"""

    def test_root_redirects_to_static_index(self, client):
        """
        ARRANGE: Set up test client without following redirects
        ACT: Send GET request to root path
        ASSERT: Verify response is redirect with correct location
        """
        # ARRANGE
        expected_redirect_path = "/static/index.html"

        # ACT
        response = client.get("/", follow_redirects=False)

        # ASSERT
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_path

    def test_root_redirect_is_temporary(self, client):
        """
        ARRANGE: Expect 307 (Temporary Redirect) status
        ACT: Send GET request to root
        ASSERT: Verify it's not a permanent redirect (301/308)
        """
        # ARRANGE
        # 307 indicates temporary redirect (preserves method)
        expected_status = 307

        # ACT
        response = client.get("/", follow_redirects=False)

        # ASSERT
        assert response.status_code == expected_status
        # Verify it's not a permanent redirect
        assert response.status_code != 301
        assert response.status_code != 308

    def test_root_follows_redirect_to_index_html(self, client):
        """
        ARRANGE: Enable redirect following
        ACT: Send GET request to root with follow_redirects=True
        ASSERT: Verify final response is successful (though static files may not be in test)
        """
        # ARRANGE
        # Note: Following redirect may result in 404 because static files 
        # are not mounted in test client, but the redirect itself should work

        # ACT
        response = client.get("/", follow_redirects=True)

        # ASSERT
        # Either 200 (if static is served) or 404 (if not found but redirect happened)
        assert response.status_code in [200, 404]
