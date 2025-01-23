import pytest
from datetime import datetime
from src.models.prospect import Prospect
from src.database.db_manager import DatabaseManager
import os

@pytest.fixture
def test_db():
    """Create a test database instance and clean up after tests."""
    # Use a test-specific database file
    test_db_path = "test_crm.db"
    db = DatabaseManager(test_db_path)
    yield db
    # Clean up: remove the test database file after tests
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

def test_add_prospect(test_db):
    """Test adding a new prospect."""
    # Arrange
    prospect = Prospect(
        id=None,
        full_name="John Doe",
        phone_number="1234567890",
        email="john@example.com",
        status="Cold Lead",
        notes="Test notes",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Act
    prospect_id = test_db.add_prospect(prospect)
    
    # Assert
    assert prospect_id > 0
    prospects = test_db.get_all_prospects()
    assert len(prospects) == 1
    assert prospects[0].full_name == "John Doe"

def test_duplicate_email(test_db):
    """Test that duplicate emails are detected."""
    # Arrange
    email = "test@example.com"
    prospect1 = Prospect(
        id=None,
        full_name="John Doe",
        phone_number="1234567890",
        email=email,
        status="Cold Lead",
        notes="Test notes",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Act & Assert
    test_db.add_prospect(prospect1)
    assert test_db.check_duplicate_email(email) == True

def test_delete_prospect(test_db):
    """Test deleting a prospect."""
    # Arrange
    prospect = Prospect(
        id=None,
        full_name="John Doe",
        phone_number="1234567890",
        email="john@example.com",
        status="Cold Lead",
        notes="Test notes",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    prospect_id = test_db.add_prospect(prospect)
    
    # Act
    result = test_db.delete_prospect(prospect_id)
    
    # Assert
    assert result == True
    prospects = test_db.get_all_prospects()
    assert len(prospects) == 0 