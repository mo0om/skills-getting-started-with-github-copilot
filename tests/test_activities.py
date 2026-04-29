from src.app import activities


def test_get_activities(client):
    # Arrange: No special setup needed

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status and response content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9  # Based on current activities


def test_get_root_redirect(client):
    # Arrange: No special setup needed

    # Act: Make GET request to / without following redirects
    response = client.get("/", follow_redirects=False)

    # Assert: Check redirect status and location
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_signup_valid(client):
    # Arrange: Choose an activity and a new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check success and participant added
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1


def test_signup_invalid_activity(client):
    # Arrange: Use a non-existent activity
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate(client):
    # Arrange: Sign up first time
    activity_name = "Programming Class"
    email = "duplicatestudent@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")  # First signup

    # Act: Try to sign up again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check 400 error for duplicate
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_delete_valid(client):
    # Arrange: First sign up a student
    activity_name = "Gym Class"
    email = "deletetest@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    initial_count = len(activities[activity_name]["participants"])

    # Act: Make DELETE request to remove signup
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check success and participant removed
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1


def test_delete_invalid_activity(client):
    # Arrange: Use a non-existent activity
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check 404 error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_delete_not_signed_up(client):
    # Arrange: Try to delete a student not signed up
    activity_name = "Art Club"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Check 400 error
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]