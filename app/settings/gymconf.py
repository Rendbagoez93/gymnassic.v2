"""
Gym Configuration Module

Manages gym-specific profile and business settings.
Provides Pydantic models for gym attributes with JSON schema validation.
"""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator


class GymContact(BaseModel):
    """Gym contact information."""

    email: EmailStr
    phone: str | None = None
    phone_secondary: str | None = None
    fax: str | None = None
    website: HttpUrl | None = None


class GymAddress(BaseModel):
    """Gym physical address."""

    street: str | None = None
    street2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str = "USA"


class DayHours(BaseModel):
    """Operating hours for a single day."""

    open: str | None = Field(None, pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    close: str | None = Field(None, pattern=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    closed: bool = False


class BusinessHours(BaseModel):
    """Weekly business hours."""

    monday: DayHours | None = None
    tuesday: DayHours | None = None
    wednesday: DayHours | None = None
    thursday: DayHours | None = None
    friday: DayHours | None = None
    saturday: DayHours | None = None
    sunday: DayHours | None = None


class SocialMedia(BaseModel):
    """Social media profile URLs."""

    facebook: HttpUrl | None = None
    instagram: HttpUrl | None = None
    twitter: HttpUrl | None = None
    youtube: HttpUrl | None = None
    linkedin: HttpUrl | None = None
    tiktok: HttpUrl | None = None


class BusinessInfo(BaseModel):
    """Legal and business information."""

    tax_id: str | None = None
    license_number: str | None = None
    established_year: int | None = Field(None, ge=1900, le=2100)


class GymCapacity(BaseModel):
    """Gym capacity settings."""

    max_members: int | None = Field(None, ge=1)
    max_concurrent_users: int | None = Field(None, ge=1)


class GymSettings(BaseModel):
    """Operational settings."""

    timezone: str = "UTC"
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    language: str = Field(default="en", pattern=r"^[a-z]{2}(-[A-Z]{2})?$")
    date_format: str = "MM/DD/YYYY"


class GymAttribute(BaseModel):
    """
    Individual gym attribute.

    Used for flexible key-value configuration beyond the standard schema.
    """

    key: str
    value: Any
    description: str | None = None


class GymConfig(BaseModel):
    """
    Complete gym configuration and profile.

    This class represents all gym-specific settings including
    business profile, contact information, and operational settings.
    """

    # Required fields
    gym_name: str = Field(..., min_length=1, max_length=100)
    contact: GymContact

    # Optional profile fields
    business_name: str | None = Field(None, max_length=150)
    tagline: str | None = Field(None, max_length=200)
    description: str | None = Field(None, max_length=1000)
    logo_url: str | None = None

    # Structured information
    address: GymAddress | None = None
    business_hours: BusinessHours | None = None
    social_media: SocialMedia | None = None
    business_info: BusinessInfo | None = None
    capacity: GymCapacity | None = None
    settings: GymSettings = Field(default_factory=GymSettings)

    # Facilities and amenities
    facilities: list[str] = Field(default_factory=list)

    # Additional custom attributes
    custom_attributes: list[GymAttribute] = Field(default_factory=list)

    @field_validator("gym_name")
    @classmethod
    def validate_gym_name(cls, v: str) -> str:
        """Validate gym name is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Gym name cannot be empty")
        return v.strip()

    @classmethod
    def from_json_file(cls, file_path: str | Path) -> "GymConfig":
        """
        Load gym configuration from a JSON file.

        Args:
            file_path: Path to JSON configuration file

        Returns:
            GymConfig: Loaded configuration

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
        """
        import json

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Gym config file not found: {file_path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return cls(**data)

    def to_json_file(self, file_path: str | Path, indent: int = 2) -> None:
        """
        Save gym configuration to a JSON file.

        Args:
            file_path: Path to save JSON file
            indent: JSON indentation level
        """
        import json

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(mode="json"), f, indent=indent)

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """
        Get a custom attribute value by key.

        Args:
            key: Attribute key
            default: Default value if not found

        Returns:
            Attribute value or default
        """
        for attr in self.custom_attributes:
            if attr.key == key:
                return attr.value
        return default

    def set_attribute(self, key: str, value: Any, description: str | None = None) -> None:
        """
        Set a custom attribute.

        Args:
            key: Attribute key
            value: Attribute value
            description: Optional description
        """
        # Remove existing attribute with same key
        self.custom_attributes = [attr for attr in self.custom_attributes if attr.key != key]

        # Add new attribute
        self.custom_attributes.append(GymAttribute(key=key, value=value, description=description))

    def get_display_address(self) -> str:
        """
        Get formatted address string.

        Returns:
            str: Formatted address or empty string
        """
        if not self.address:
            return ""

        parts = []
        if self.address.street:
            parts.append(self.address.street)
        if self.address.street2:
            parts.append(self.address.street2)

        city_state_zip = []
        if self.address.city:
            city_state_zip.append(self.address.city)
        if self.address.state:
            city_state_zip.append(self.address.state)
        if self.address.postal_code:
            city_state_zip.append(self.address.postal_code)

        if city_state_zip:
            parts.append(", ".join(city_state_zip))

        if self.address.country:
            parts.append(self.address.country)

        return ", ".join(parts)

    def is_open_on_day(self, day: str) -> bool:
        """
        Check if gym is open on a specific day.

        Args:
            day: Day name (lowercase, e.g., 'monday')

        Returns:
            bool: True if open, False if closed or no hours defined
        """
        if not self.business_hours:
            return False

        day_hours = getattr(self.business_hours, day.lower(), None)
        if not day_hours:
            return False

        return not day_hours.closed and day_hours.open is not None

    def get_day_hours(self, day: str) -> str:
        """
        Get formatted hours string for a day.

        Args:
            day: Day name (lowercase, e.g., 'monday')

        Returns:
            str: Formatted hours (e.g., '06:00 - 22:00') or 'Closed'
        """
        if not self.business_hours:
            return "Hours not set"

        day_hours = getattr(self.business_hours, day.lower(), None)
        if not day_hours:
            return "Hours not set"

        if day_hours.closed:
            return "Closed"

        if day_hours.open and day_hours.close:
            return f"{day_hours.open} - {day_hours.close}"

        return "Hours not set"
