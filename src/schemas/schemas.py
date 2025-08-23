from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, AliasPath, field_validator


class ServingClassSchema(BaseModel):
    free_places: int = Field(alias="places")
    class_service: str = Field(alias="classservice")
    prices: list[float] = Field(alias="prices")


class PlacesSchema(BaseModel):
    type: int = Field(alias="car_type")
    serving_class: list[ServingClassSchema] = Field(alias="price_multi")

    @field_validator('type', mode='after')
    @classmethod
    def convert_train_type(cls, v: int) -> str:
        train_types = {
            1: "Общий",
            2: "Сидячий",
            3: "Плацкартный",
            4: "Купейный",
            5: "Мягкий",
            6: "СВ"
        }
        return train_types.get(v, "Неизвестный тип места")


class TrainSchema(BaseModel):
    from_: str = Field(alias="from_station_db")
    to: str = Field(alias="to_station_db")
    type: str = Field(alias="train_type")
    is_left: bool = Field(alias="is_left")
    number: str = Field(alias="train_number")
    dep_time: datetime = Field(alias="from_time_formatted")
    arr_time: datetime = Field(alias="to_time_formatted")
    places: list[PlacesSchema] = Field()
    
    @field_validator("dep_time", "arr_time", mode='before')
    @classmethod
    def local_to_utc(cls, time: str) -> datetime:
        local_dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        local_dt = local_dt.replace(tzinfo=ZoneInfo("Europe/Minsk"))
        utc_dt = local_dt.astimezone(timezone.utc)
        return utc_dt

    def __str__(self) -> str:
        utc_dt = self.dep_time.replace(tzinfo=timezone.utc)
        local_dt = utc_dt.astimezone(ZoneInfo("Europe/Minsk"))
        local_str = datetime.strftime(local_dt, "%d.%m.%Y %H:%M:%S")
        return f"{self.from_} -> {self.to}, {self.type} ({self.number}, {local_str})"

    # TODO add type field validation


class RouteSchema(BaseModel):
    from_: str = Field(validation_alias=AliasPath("from", "st_name_ru"))
    to: str = Field(validation_alias=AliasPath("to", "st_name_ru"))
    trains: list[TrainSchema] = Field(alias="routes")
