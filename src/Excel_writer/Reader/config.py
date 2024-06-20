from enum import Enum
from typing import Type, Tuple
from DB_module.models import Mlexcel_model, Operation


__all__ = [
    "cl_setting",
    "md_setting",
]


class MD_Settings(Enum):
    Ml_ex: Type[Mlexcel_model] = Mlexcel_model
    Op_ex: Type[Operation] = Operation


class CL_Settings(Enum):
    Ml_ex = (
        "Заказ",
        "Маршрутный лист",
        "№ детали",
        "Количество",
        "Норм/часы",
        "Дата распечатки",
        "Тип сдачи",
        "Дата изготовления",
        "Название детали",
        "Норма расхода на ед",
        "Масса детали",
        "Материал", 
        "Профиль заготовки",
        "Профиль",
        "Деталей из заготовки",
    )

    Op_ex: Tuple[str, ...] = (
        "№ детали", "Номер операции",
        "Название операции", "Тпз",
        "Тшт",
    )


cl_setting = CL_Settings
md_setting = MD_Settings
