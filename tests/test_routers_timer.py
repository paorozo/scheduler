# from fastapi.testclient import TestClient
# from unittest.mock import MagicMock
# import pytest
#
# from main import app
# from models.task import Task
# from datetime import datetime, timedelta, timezone
#
# client = TestClient(app)
#
#
# @pytest.fixture
# def mock_db_session():
#     return MagicMock()
#
#
# def test_set_timer(mock_db_session, monkeypatch):
#     task_mock = Task(
#         id=1,
#         created_at=datetime.now(timezone.utc),
#         expiration_time=datetime.now(timezone.utc),
#         url="http://example.com",
#     )
#     task_mock.time_left = MagicMock(return_value=3600)
#
#     monkeypatch.setattr("models.task.create_task", MagicMock(return_value=task_mock))
#
#     response = client.post(
#         "/timer",
#         params={"hours": 1, "minutes": 0, "seconds": 0, "url": "http://example.com"},
#     )
#     response_json = response.json()
#
#     assert response.status_code == 200
#     assert isinstance(response_json["id"], int) and response_json["id"] > 0
#
#
# def test_get_timer(mock_db_session, monkeypatch):
#     task_mock = Task(
#         id=1,
#         created_at=datetime.now(timezone.utc),
#         expiration_time=datetime.now(timezone.utc) + timedelta(hours=1),
#         url="http://example.com",
#     )
#
#     task_mock.time_left = lambda: 3600
#
#     monkeypatch.setattr("models.task.get_task", MagicMock(return_value=task_mock))
#
#     response = client.get(
#         "/timer/1",
#     )
#     response_json = response.json()
#
#     assert response.status_code == 200
#     print(f"JSON RESPONSE {response_json}")
