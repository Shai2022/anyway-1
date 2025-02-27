from enum import Enum
from typing import List, Union
import logging
import math

try:
    from flask_babel import _
except ModuleNotFoundError:

    def _(str):
        return str


class VehicleType(Enum):
    CAR = 1
    TRUCK_UPTO_4 = 2
    PICKUP_UPTO_4 = 3
    TRUCK_4_TO_10 = 4
    TRUCK_12_TO_16 = 5
    TRUCK_16_TO_34 = 6
    TRUCK_ABOVE_34 = 7
    MOTORCYCLE_UPTO_50 = 8
    MOTORCYCLE_50_TO_250 = 9
    MOTORCYCLE_250_TO_500 = 10
    BUS = 11
    TAXI = 12
    WORK = 13
    TRACTOR = 14
    BIKE = 15
    TRAIN = 16
    OTHER_AND_UNKNOWN = 17
    MINIBUS = 18
    MOTORCYCLE_ABOVE_500 = 19
    ELECTRIC_SCOOTER = 21
    MOBILITY_SCOOTER = 22
    ELECTRIC_BIKE = 23
    TRUCK_3_5_TO_10 = 24
    TRUCK_10_TO_12 = 25

    def get_categories(self) -> List[int]:
        res = []
        for t in list(VehicleCategory):
            if self in t.value:
                res.append(t)
        return res

    def get_english_display_name(self):
        english_vehicle_type_display_names = {
            VehicleType.CAR: "private car",
            VehicleType.TRUCK_UPTO_4: "truck upto 4 tons",
            VehicleType.PICKUP_UPTO_4: "pickup upto 4 tons",
            VehicleType.TRUCK_4_TO_10: "truck 4 to 10 tons",
            VehicleType.TRUCK_12_TO_16: "truck 12 to 16 tons",
            VehicleType.TRUCK_16_TO_34: "truck 16 to 34 tons",
            VehicleType.TRUCK_ABOVE_34: "truck above 34 tons",
            VehicleType.MOTORCYCLE_UPTO_50: "motorcycle upto 50 cc",
            VehicleType.MOTORCYCLE_50_TO_250: "motorcycle 50 to 250 cc",
            VehicleType.MOTORCYCLE_250_TO_500: "motorcycle 250 to 500 cc",
            VehicleType.BUS: "bus",
            VehicleType.TAXI: "taxi",
            VehicleType.WORK: "work vehicle",
            VehicleType.TRACTOR: "tractor",
            VehicleType.BIKE: "bike",
            VehicleType.TRAIN: "train",
            VehicleType.OTHER_AND_UNKNOWN: "other and unknown",
            VehicleType.MINIBUS: "minibus",
            VehicleType.MOTORCYCLE_ABOVE_500: "motorcycle above 500 cc",
            VehicleType.ELECTRIC_SCOOTER: "electric scooter",
            VehicleType.MOBILITY_SCOOTER: "mobility scooter",
            VehicleType.ELECTRIC_BIKE: "electric bike",
            VehicleType.TRUCK_3_5_TO_10: "truck 3.5 to 10 tons",
            VehicleType.TRUCK_10_TO_12: "truck 10 to 12 tons",
        }
        try:
            return english_vehicle_type_display_names[self]
        except (KeyError, TypeError):
            logging.exception(f"VehicleType.get_display_name: {self}: no display string defined")
            return "no display name defined"

    @staticmethod
    def to_type_code(db_val: Union[float, int]) -> int:
        """Values read from DB may arrive as float, and empty values come as nan"""
        if isinstance(db_val, float):
            if math.isnan(db_val):
                return VehicleType.OTHER_AND_UNKNOWN.value
            else:
                return int(db_val)
        elif isinstance(db_val, int):
            return db_val
        else:
            logging.error(
                f"VehicleType.fo_type_code: unknown value: {db_val}({type(db_val)})"
                ". returning OTHER_AND_UNKNOWN"
            )
            return VehicleType.OTHER_AND_UNKNOWN.value


VT = VehicleType


class VehicleCategory(Enum):
    PROFESSIONAL_DRIVER = 1
    PRIVATE_DRIVER = 2
    LIGHT_ELECTRIC = 3
    CAR = 4
    LARGE = 5
    MOTORCYCLE = 6
    BICYCLE_AND_SMALL_MOTOR = 7
    OTHER = 8

    def get_codes(self) -> List[int]:
        """returns VehicleType codes of category"""
        category_vehicle_types = {
            VehicleCategory.PROFESSIONAL_DRIVER: [
                VehicleType.TRUCK_UPTO_4,
                VehicleType.PICKUP_UPTO_4,
                VehicleType.TRUCK_4_TO_10,
                VehicleType.TRUCK_12_TO_16,
                VehicleType.TRUCK_16_TO_34,
                VehicleType.TRUCK_ABOVE_34,
                VehicleType.BUS,
                VehicleType.TAXI,
                VehicleType.WORK,
                VehicleType.TRACTOR,
                VehicleType.MINIBUS,
                VehicleType.TRUCK_3_5_TO_10,
                VehicleType.TRUCK_10_TO_12,
            ],
            VehicleCategory.PRIVATE_DRIVER: [
                VehicleType.CAR,
                VehicleType.MOTORCYCLE_UPTO_50,
                VehicleType.MOTORCYCLE_50_TO_250,
                VehicleType.MOTORCYCLE_250_TO_500,
                VehicleType.MOTORCYCLE_ABOVE_500,
            ],
            VehicleCategory.LIGHT_ELECTRIC: [
                VehicleType.ELECTRIC_SCOOTER,
                VehicleType.MOBILITY_SCOOTER,
                VehicleType.ELECTRIC_BIKE,
            ],
            VehicleCategory.CAR: [VehicleType.CAR, VehicleType.TAXI],
            VehicleCategory.LARGE: [
                VehicleType.TRUCK_UPTO_4,
                VehicleType.PICKUP_UPTO_4,
                VehicleType.TRUCK_4_TO_10,
                VehicleType.TRUCK_12_TO_16,
                VehicleType.TRUCK_16_TO_34,
                VehicleType.TRUCK_ABOVE_34,
                VehicleType.BUS,
                VehicleType.WORK,
                VehicleType.TRACTOR,
                VehicleType.MINIBUS,
                VehicleType.TRUCK_3_5_TO_10,
                VehicleType.TRUCK_10_TO_12,
            ],
            VehicleCategory.MOTORCYCLE: [
                VehicleType.MOTORCYCLE_UPTO_50,
                VehicleType.MOTORCYCLE_50_TO_250,
                VehicleType.MOTORCYCLE_250_TO_500,
                VehicleType.MOTORCYCLE_ABOVE_500,
            ],
            VehicleCategory.BICYCLE_AND_SMALL_MOTOR: [
                VehicleType.BIKE,
                VehicleType.ELECTRIC_SCOOTER,
                VehicleType.ELECTRIC_BIKE,
            ],
            VehicleCategory.OTHER: [
                VehicleType.BIKE,
                VehicleType.TRAIN,
                VehicleType.OTHER_AND_UNKNOWN,
            ],
        }
        return list(map(lambda x: x.value, category_vehicle_types[self]))

    def contains(self, vt_code: int) -> bool:
        # noinspection PyTypeChecker
        if not isinstance(int, vt_code):
            logging.warning(f"VehicleCategory.contains: {vt_code}:{type(vt_code)}: not int")
            return False
        return vt_code in self.get_codes()

    def get_english_display_name(self):
        english_vehicle_type_display_names = {
            VehicleCategory.PROFESSIONAL_DRIVER: "professional driver",
            VehicleCategory.PRIVATE_DRIVER: "private driver",
            VehicleCategory.LIGHT_ELECTRIC: "light electric vehicles",
            VehicleCategory.CAR: "private car",
            VehicleCategory.LARGE: "large vehicle",
            VehicleCategory.MOTORCYCLE: "motorcycle",
            VehicleCategory.BICYCLE_AND_SMALL_MOTOR: "bicycle and small motor vehicles",
            VehicleCategory.OTHER: "other vehicle",
        }
        try:
            return english_vehicle_type_display_names[self]
        except (KeyError, TypeError):
            logging.exception(f"VehicleType.get_display_name: {self}: no display string defined")
            return "no display name defined"


_("professional driver")
_("private driver")
_("light electric vehicles")
_("private car")
_("large vehicle")
_("motorcycle")
_("bicycle and small motor vehicles")
_("other vehicle")
