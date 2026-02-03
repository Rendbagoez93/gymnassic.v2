"""
Tests for Gym Configuration Module

Tests GymConfig and GymAttribute classes to ensure proper
validation, JSON serialization, and business logic.
"""

import json

import pytest
from pydantic import ValidationError

from app.settings.gymconf import (
    BusinessHours,
    BusinessInfo,
    DayHours,
    GymAddress,
    GymAttribute,
    GymCapacity,
    GymConfig,
    GymContact,
    GymSettings,
    SocialMedia,
)


class TestGymContact:
    """Test GymContact model."""

    def test_valid_contact(self):
        """Test creating valid contact information."""
        contact = GymContact(
            email="test@gym.com",
            phone="+1-555-0100",
            website="https://www.gym.com",
        )
        assert contact.email == "test@gym.com"
        assert contact.phone == "+1-555-0100"
        assert str(contact.website) == "https://www.gym.com/"

    def test_invalid_email(self):
        """Test that invalid email raises validation error."""
        with pytest.raises(ValidationError):
            GymContact(email="invalid-email")

    def test_optional_fields(self):
        """Test that phone and website are optional."""
        contact = GymContact(email="test@gym.com")
        assert contact.phone is None
        assert contact.website is None


class TestGymAddress:
    """Test GymAddress model."""

    def test_full_address(self):
        """Test creating complete address."""
        address = GymAddress(
            street="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
        )
        assert address.street == "123 Main St"
        assert address.city == "New York"
        assert address.country == "USA"

    def test_default_country(self):
        """Test default country is USA."""
        address = GymAddress()
        assert address.country == "USA"


class TestDayHours:
    """Test DayHours model."""

    def test_valid_hours(self):
        """Test valid business hours."""
        hours = DayHours(open="09:00", close="17:00")
        assert hours.open == "09:00"
        assert hours.close == "17:00"
        assert hours.closed is False

    def test_closed_day(self):
        """Test closed day."""
        hours = DayHours(closed=True)
        assert hours.closed is True
        assert hours.open is None

    def test_invalid_time_format(self):
        """Test invalid time format raises error."""
        with pytest.raises(ValidationError):
            DayHours(open="25:00")  # Invalid hour

        with pytest.raises(ValidationError):
            DayHours(close="12:60")  # Invalid minute


class TestBusinessHours:
    """Test BusinessHours model."""

    def test_weekly_hours(self):
        """Test setting hours for all days."""
        hours = BusinessHours(
            monday=DayHours(open="06:00", close="22:00"),
            tuesday=DayHours(open="06:00", close="22:00"),
            sunday=DayHours(closed=True),
        )
        assert hours.monday.open == "06:00"
        assert hours.sunday.closed is True


class TestSocialMedia:
    """Test SocialMedia model."""

    def test_social_profiles(self):
        """Test social media URLs."""
        social = SocialMedia(
            facebook="https://facebook.com/gym",
            instagram="https://instagram.com/gym",
        )
        assert str(social.facebook) == "https://facebook.com/gym"
        assert social.twitter is None


class TestBusinessInfo:
    """Test BusinessInfo model."""

    def test_business_details(self):
        """Test business information."""
        info = BusinessInfo(
            tax_id="12-3456789",
            license_number="GYM-12345",
            established_year=2020,
        )
        assert info.tax_id == "12-3456789"
        assert info.established_year == 2020

    def test_year_validation(self):
        """Test year must be in valid range."""
        with pytest.raises(ValidationError):
            BusinessInfo(established_year=1800)  # Too old

        with pytest.raises(ValidationError):
            BusinessInfo(established_year=2200)  # Too far in future


class TestGymCapacity:
    """Test GymCapacity model."""

    def test_capacity_limits(self):
        """Test capacity settings."""
        capacity = GymCapacity(max_members=1000, max_concurrent_users=150)
        assert capacity.max_members == 1000
        assert capacity.max_concurrent_users == 150

    def test_positive_values_required(self):
        """Test capacity must be positive."""
        with pytest.raises(ValidationError):
            GymCapacity(max_members=0)


class TestGymSettings:
    """Test GymSettings model."""

    def test_default_settings(self):
        """Test default operational settings."""
        settings = GymSettings()
        assert settings.timezone == "UTC"
        assert settings.currency == "USD"
        assert settings.language == "en"

    def test_custom_settings(self):
        """Test custom settings."""
        settings = GymSettings(
            timezone="America/New_York",
            currency="EUR",
            language="en-US",
        )
        assert settings.timezone == "America/New_York"
        assert settings.currency == "EUR"

    def test_currency_validation(self):
        """Test currency must be 3 uppercase letters."""
        with pytest.raises(ValidationError):
            GymSettings(currency="US")  # Too short

        with pytest.raises(ValidationError):
            GymSettings(currency="usd")  # Lowercase


class TestGymAttribute:
    """Test GymAttribute model."""

    def test_basic_attribute(self):
        """Test creating custom attribute."""
        attr = GymAttribute(key="theme_color", value="#FF5733")
        assert attr.key == "theme_color"
        assert attr.value == "#FF5733"
        assert attr.description is None

    def test_attribute_with_description(self):
        """Test attribute with description."""
        attr = GymAttribute(
            key="max_age",
            value=65,
            description="Maximum age for membership",
        )
        assert attr.description == "Maximum age for membership"


class TestGymConfig:
    """Test GymConfig model."""

    def test_minimal_config(self):
        """Test creating config with minimal required fields."""
        config = GymConfig(
            gym_name="Test Gym",
            contact=GymContact(email="test@gym.com"),
        )
        assert config.gym_name == "Test Gym"
        assert config.contact.email == "test@gym.com"

    def test_full_config(self):
        """Test creating complete configuration."""
        config = GymConfig(
            gym_name="Complete Gym",
            business_name="Complete Gym LLC",
            tagline="Get Fit Today",
            description="A full-service gym",
            contact=GymContact(
                email="info@completegym.com",
                phone="+1-555-0100",
            ),
            address=GymAddress(
                street="123 Gym St",
                city="Fitness City",
                state="FC",
                postal_code="12345",
            ),
            facilities=["Weights", "Cardio", "Pool"],
            settings=GymSettings(timezone="America/New_York"),
        )
        assert config.gym_name == "Complete Gym"
        assert len(config.facilities) == 3
        assert config.settings.timezone == "America/New_York"

    def test_empty_gym_name_validation(self):
        """Test that empty gym name is rejected."""
        with pytest.raises(ValidationError):
            GymConfig(
                gym_name="",
                contact=GymContact(email="test@gym.com"),
            )

        with pytest.raises(ValidationError):
            GymConfig(
                gym_name="   ",  # Whitespace only
                contact=GymContact(email="test@gym.com"),
            )

    def test_gym_name_trimming(self):
        """Test that gym name is trimmed."""
        config = GymConfig(
            gym_name="  Test Gym  ",
            contact=GymContact(email="test@gym.com"),
        )
        assert config.gym_name == "Test Gym"

    def test_custom_attributes(self):
        """Test custom attributes functionality."""
        config = GymConfig(
            gym_name="Test Gym",
            contact=GymContact(email="test@gym.com"),
        )

        # Set attribute
        config.set_attribute("loyalty_program", True, "Enable loyalty rewards")
        assert config.get_attribute("loyalty_program") is True

        # Get non-existent attribute
        assert config.get_attribute("non_existent") is None
        assert config.get_attribute("non_existent", "default") == "default"

        # Update existing attribute
        config.set_attribute("loyalty_program", False)
        assert config.get_attribute("loyalty_program") is False

    def test_get_display_address(self):
        """Test formatted address display."""
        # Empty address
        config = GymConfig(
            gym_name="Test Gym",
            contact=GymContact(email="test@gym.com"),
        )
        assert config.get_display_address() == ""

        # Full address
        config.address = GymAddress(
            street="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="USA",
        )
        address = config.get_display_address()
        assert "123 Main St" in address
        assert "New York" in address
        assert "NY" in address
        assert "10001" in address

    def test_is_open_on_day(self):
        """Test checking if gym is open on specific day."""
        config = GymConfig(
            gym_name="Test Gym",
            contact=GymContact(email="test@gym.com"),
            business_hours=BusinessHours(
                monday=DayHours(open="09:00", close="17:00"),
                sunday=DayHours(closed=True),
            ),
        )

        assert config.is_open_on_day("monday") is True
        assert config.is_open_on_day("sunday") is False
        assert config.is_open_on_day("tuesday") is False  # Not defined

    def test_get_day_hours(self):
        """Test getting formatted hours for a day."""
        config = GymConfig(
            gym_name="Test Gym",
            contact=GymContact(email="test@gym.com"),
            business_hours=BusinessHours(
                monday=DayHours(open="09:00", close="17:00"),
                sunday=DayHours(closed=True),
            ),
        )

        assert config.get_day_hours("monday") == "09:00 - 17:00"
        assert config.get_day_hours("sunday") == "Closed"
        assert config.get_day_hours("tuesday") == "Hours not set"


class TestGymConfigFileOperations:
    """Test GymConfig file I/O operations."""

    def test_to_json_file(self, tmp_path):
        """Test saving config to JSON file."""
        config = GymConfig(
            gym_name="Test Gym",
            contact=GymContact(
                email="test@gym.com",
                phone="+1-555-0100",
            ),
            facilities=["Weights", "Cardio"],
        )

        file_path = tmp_path / "test_gym.json"
        config.to_json_file(file_path)

        assert file_path.exists()

        # Verify file content
        with open(file_path) as f:
            data = json.load(f)

        assert data["gym_name"] == "Test Gym"
        assert data["contact"]["email"] == "test@gym.com"
        assert "Weights" in data["facilities"]

    def test_from_json_file(self, tmp_path):
        """Test loading config from JSON file."""
        # Create test JSON file
        test_data = {
            "gym_name": "Loaded Gym",
            "contact": {
                "email": "loaded@gym.com",
                "phone": "+1-555-0200",
            },
            "facilities": ["Pool", "Sauna"],
        }

        file_path = tmp_path / "loaded_gym.json"
        with open(file_path, "w") as f:
            json.dump(test_data, f)

        # Load config
        config = GymConfig.from_json_file(file_path)

        assert config.gym_name == "Loaded Gym"
        assert config.contact.email == "loaded@gym.com"
        assert "Pool" in config.facilities

    def test_from_json_file_not_found(self):
        """Test loading from non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            GymConfig.from_json_file("/non/existent/path.json")

    def test_roundtrip_json(self, tmp_path):
        """Test saving and loading config preserves data."""
        original = GymConfig(
            gym_name="Roundtrip Gym",
            business_name="Roundtrip LLC",
            tagline="Test Roundtrip",
            contact=GymContact(
                email="roundtrip@gym.com",
                website="https://roundtrip.com",
            ),
            address=GymAddress(
                street="456 Test Ave",
                city="Test City",
                state="TC",
            ),
            facilities=["Equipment A", "Equipment B"],
            settings=GymSettings(
                timezone="America/Chicago",
                currency="USD",
            ),
        )

        # Save
        file_path = tmp_path / "roundtrip.json"
        original.to_json_file(file_path)

        # Load
        loaded = GymConfig.from_json_file(file_path)

        # Compare
        assert loaded.gym_name == original.gym_name
        assert loaded.business_name == original.business_name
        assert loaded.tagline == original.tagline
        assert loaded.contact.email == original.contact.email
        assert loaded.address.street == original.address.street
        assert loaded.facilities == original.facilities
        assert loaded.settings.timezone == original.settings.timezone
