from copy import copy
from enum import Enum

from typing import Dict, Any


__all__ = [
    "Cl_type",
]


class Formating(Enum):
    text: Dict[str, Any] = {
        'font_name': "Time New Roman",
        'font_size': 9,
        'align': "left",
        "valign": "vcenter",
    }
    int = copy(text)
    int.update({
        'align': "center",
        "num_format": "# ##0"
    })

    float = copy(text)
    float.update({
        "align": "center",
        "num_format": r"#,##0.000"
    })

    date = copy(text)
    date.update({
        "align": "center",
        "num_format": "d mmmm yyyy"
    })

    header = copy(text)
    header.update({
        "font_size": 12,
        "align": "center",
        "bold": True,
    })


Cl_type = {
    "Заказ": Formating.text.value,
    "Маршрутный лист": Formating.text.value,
    "№ детали": Formating.text.value,
    "Количество": Formating.int.value,
    "Норм/часы": Formating.float.value,
    "Дата распечатки": Formating.date.value,
    "Тип сдачи": Formating.text.value,
    "Дата изготовления": Formating.date.value,
    "Название детали": Formating.text.value,
    "Норма расхода на ед": Formating.float.value,
    "Масса детали": Formating.float.value,
    "Материал": Formating.text.value,
    "Профиль заготовки": Formating.text.value,
    "Профиль": Formating.text.value,
    "Деталей из заготовки": Formating.int.value,
}
