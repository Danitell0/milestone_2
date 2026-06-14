#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError
import datetime as dt


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: dt.datetime
    is_operational: bool = True
    notes: None | str = Field(None, max_length=200)


def display_info(station: SpaceStation) -> None:
    print(f"ID: {station.station_id}\n"
          f"Name: {station.name}\n"
          f"Crew: {station.crew_size} people\n"
          f"Power: {station.power_level}%\n"
          f"Oxygen: {station.oxygen_level}%\n"
          f"Status: ", end="")
    if station.is_operational:
        print("Operational")
    else:
        print("Non-operational")
    if station.notes:
        print(f"Notes: {station.notes}")


def main() -> None:
    skylab_b = SpaceStation(
        station_id="NASA001",
        name="Skylab B",
        crew_size=3,
        power_level=67.5,
        oxygen_level=23.5,
        last_maintenance=dt.datetime(1976, 5, 8),
        is_operational=False,
        notes="Lack of funding, now a museum piece."
    )
    print("Space Station Data Validation")
    print("=====================================")
    display_info(skylab_b)
    print("\n=====================================")
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="VAST001",
            name="Haven-2",
            crew_size=500,
            power_level=67.5,
            oxygen_level=23.5,
            last_maintenance=dt.datetime(2028, 12, 25),
            is_operational=True,
            notes="Schedule to be launched."
        )
    except ValidationError as e:
        print(e.errors()[0].get('msg'))


if __name__ == "__main__":
    main()
