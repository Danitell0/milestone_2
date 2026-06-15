#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
import datetime as dt


class ContactType(Enum):
    radio = 'radio'
    visual = 'visual'
    physical = 'physical'
    telepathic = 'telepathic'


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: dt.datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: None | str = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def contact_check(self) -> 'AlienContact':
        if not self.contact_id.startswith('AC'):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.telepathic
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires "
                             "at least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) "
                             "should include received messages")
        return self


def display_contact(contact: AlienContact) -> None:
    print(f"ID: {contact.contact_id}\n"
          f"Type: {contact.contact_type.value}\n"
          f"Location: {contact.location}\n"
          f"Signal: {contact.signal_strength}/10\n"
          f"Duration: {contact.duration_minutes} minutes\n"
          f"Witnesses: {contact.witness_count}\n"
          f"Message: {contact.message_received}")


def main() -> None:
    first_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=dt.datetime(2024, 8, 5),
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="'Greetings from Zeta Reticuli'",
        is_verified=True
    )
    print("Alien Contact Log Validation")
    print("======================================")
    display_contact(first_contact)
    print("\n======================================")
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2026_001",
            timestamp=dt.datetime(2026, 8, 5),
            location="Here at Codam",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="",
            is_verified=False
        )
    except ValidationError as e:
        print(e.errors()[0].get('msg').removeprefix('Value error, '))


if __name__ == "__main__":
    main()
