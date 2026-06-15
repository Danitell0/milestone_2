#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
import datetime as dt


class Rank(Enum):
    cadet = 'cadet'
    officer = 'officer'
    lieutenant = 'lieutenant'
    captain = 'captain'
    commander = 'commander'


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: dt.datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember]
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_check(self) -> 'SpaceMission':
        if not self.mission_id.startswith('M'):
            raise ValueError("Mission ID must start with 'M'")
        if not any(member.rank == Rank.commander
                   or member.rank == Rank.captain for member in self.crew):
            raise ValueError("Mission must have at "
                             "least one Commander or Captain")
        if self.duration_days > 365:
            above_5 = sum(member.years_experience >= 5 for member in self.crew)
            if above_5 / len(self.crew) < 0.5:
                raise ValueError("Long missions (> 365 days) need "
                                 "50% experienced crew (5+ years)")
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def display_mission(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}\n"
          f"ID: {mission.mission_id}\n"
          f"Destination: {mission.destination}\n"
          f"Duration: {mission.duration_days} days\n"
          f"Budget: ${mission.budget_millions}M\n"
          f"Crew size: {len(mission.crew)}\n", end="")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value})"
              f" - {member.specialization}")


def main() -> None:

    sarah_connor = CrewMember(
        member_id="SC001",
        name="Sarah Connor",
        rank=Rank.commander,
        age=42,
        specialization="Mission Command",
        years_experience=15,
        is_active=True
    )
    john_smith = CrewMember(
        member_id="JS002",
        name="John Smith",
        rank=Rank.lieutenant,
        age=57,
        specialization="Navigation",
        years_experience=30,
        is_active=True
    )
    alice_johnson = CrewMember(
        member_id="AJ003",
        name="Alice Johnson",
        rank=Rank.officer,
        age=33,
        specialization="Engineering",
        years_experience=6,
        is_active=True
    )
    mission_42 = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=dt.datetime(2024, 6, 7),
        duration_days=900,
        crew=[sarah_connor, john_smith, alice_johnson],
        mission_status="Lost in Space",
        budget_millions=2500.0
    )
    print("Space Mission Crew Validation")
    print("=========================================")
    display_mission(mission_42)
    print("\n=========================================")
    daniel = CrewMember(
        member_id="DF000",
        name="Daniel Fernandes",
        rank=Rank.cadet,
        age=27,
        specialization="Nothing at all",
        years_experience=1,
        is_active=True
    )
    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2026_CODAM",
            mission_name="Set To Fail",
            destination="Codam",
            launch_date=dt.datetime(2026, 3, 19),
            duration_days=999,
            crew=[daniel],
            mission_status="",
            budget_millions=1.0
        )
    except ValidationError as e:
        print(e.errors()[0].get('msg').removeprefix('Value error, '))


if __name__ == "__main__":
    main()
