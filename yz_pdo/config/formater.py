from dataclasses import dataclass


@dataclass
class Formater(object):

    format_number = {
        'num_format': '#,##0.000',
        "align": "right",
        "valign": "vcenter",
        "font_name": "Calibri",
        "font_size": 11,
    }

    format_procent = {
        'num_format': '##0.00 %',
        "align": "right",
        "valign": "vcenter",
        "font_name": "Calibri",
        "font_size": 11,
    }

    format_int = {
        'num_format': r"#,##0",
        "align": "right",
        "valign": "vcenter",
        "font_name": "Calibri",
        "font_size": 11,
    }

    format_date = {
        "num_format": "DD.MM.YYYY",
        "align": "vcenter",
        "valign": "vcenter",
        "font_name": "Calibri",
        "font_size": 11,
    }

    text_center = {
        "align": "center",
        "valign": "vcenter",
        "font_name": "Calibri",
        "font_size": 11,
        'text_wrap': True,
    }

    text_basic = {
        "align": "left",
        "valign": "vcenter",
        "font_name": "Calibri",
        "font_size": 11,
        'text_wrap': True,
    }
