"""
Basic example of a Vehicle registration system.
"""
from dataclasses import dataclass
from os import strerror
from random import *
from string import *
from typing import Optional


@dataclass
class VehicleInfoMissingError(Exception):
    """Custom error that is raised when vehicle information is missing for a particular brand."""

    brand: str
    model: str
    message: str = "Vehicle information is missing."


@dataclass
class VehicleInfo:
    """Class that contains basic information about a vehicle. Used for registering new vehicles."""

    brand: str
    model: str
    electric: bool
    catalogue_price: int
    production_year: int

    def compute_tax(self) -> float:
        """Computes the tax to be paid when registering a vehicle of this type."""
        tax_percentage = 0.05
        if self.electric:
            tax_percentage = 0.02
        return tax_percentage * self.catalogue_price

    def get_info_str(self) -> str:
        """Returns a string representation of this instance."""
        tax = self.compute_tax()
        return f"brand: {self.brand} - type: {self.model} - tax: {tax}"


class Vehicle:
    """Class representing a vehicle (electric or fossil fuel)."""

    def __init__(self, _id: str, license_plate: str, info: VehicleInfo) -> None:
        self._id = _id
        self.license_plate = license_plate
        self.info = info

    def to_string(self) -> strerror:
        """Returns a string representation of this instance."""
        info_str = self.info.get_info_str()
        return f"Id: {self._id}. License plate: {self.license_plate}. Info: {info_str}."


def add_vehicle_info(
    brand: str,
    model: str,
    electric: bool,
    catalogue_price: int,
    year: int,
    vehicle_list: list[VehicleInfo] = [],
) -> list[VehicleInfo]:
    """Helper method for adding a VehicleInfo object to a list."""
    vehicle_list.append(VehicleInfo(brand, model, electric, catalogue_price, year))
    return vehicle_list


class VehicleRegistry:
    """Class representing a basic vehicle registration system."""

    def __init__(self) -> None:
        self.vehicle_info: list[VehicleInfo] = []

        # add various entries containing information about vehicles
        add_vehicle_info("Tesla", "Model 3", True, 50000, 2021, self.vehicle_info)
        add_vehicle_info("Volkswagen", "ID3", True, 35000, 2021, self.vehicle_info)
        add_vehicle_info("BMW", "520e", False, 60000, 2021, self.vehicle_info)
        add_vehicle_info("Tesla", "Model Y", True, 55000, 2021, self.vehicle_info)

        self.online = True

    def generate_vehicle_id(self, length: int) -> str:
        """Helper method for generating a random vehicle id."""
        return "".join(choices(ascii_uppercase, k=length))

    def generate_vehicle_license(self, _id: str) -> str:
        """Helper method for generating a vehicle license number."""
        return f"{_id[:2]}-{''.join(choices(digits, k=2))}-{''.join(choices(ascii_uppercase, k=2))}"

    def create_vehicle(self, brand: str, model: str) -> Vehicle:
        """Creates a new vehicle and generates an id and a license plate."""
        for vehicle_info in self.vehicle_info:
            if vehicle_info.brand == brand:
                if vehicle_info.model == model:
                    vehicle_id = self.generate_vehicle_id(12)
                    license_plate = self.generate_vehicle_license(vehicle_id)
                    return Vehicle(vehicle_id, license_plate, vehicle_info)
        raise VehicleInfoMissingError(brand, model)

    def online_status(self) -> str:
        """Reports whether the registry system is online."""
        return (
            "Offline"
            if not self.online
            else "Connection error"
            if len(self.vehicle_info) == 0
            else "Online"
        )


def main() -> None:
    """Main function."""

    # create a registry instance
    registry = VehicleRegistry()

    # verify that the registry is online
    print(f"Registry status: {registry.online_status()}")

    vehicle = registry.create_vehicle("Volkswagen", "ID3")

    # print(add_vehicle_info("Tesla", "Model 3", True, 50000, 2021))
    # print(add_vehicle_info("Tesla", "Model 3", True, 50000, 2021))

    # print out the vehicle information
    print(vehicle.to_string())


if __name__ == "__main__":
    main()
