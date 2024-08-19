from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def mock_db():
    return Mock(Session)
