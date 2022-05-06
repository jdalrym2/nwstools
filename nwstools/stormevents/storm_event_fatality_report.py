#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pathlib
from typing import Optional, Union
from datetime import datetime
from dataclasses import dataclass

from .utils import to_datetime


@dataclass
class StormEventFatalityReport:
    """ Class to store a storm event fatality report the NOAA NCEI Storm Events Database """
    event_id: int
    fatality_id: int
    fatality_time: datetime
    fatality_type: str
    fatality_age: Optional[int]
    fatality_sex: Optional[str]
    fatality_location: str

    @classmethod
    def from_csv(cls, csv_file: Union[str, pathlib.Path]):
        """ Load a set of fatality reports from a CSV file """
        cls_list = []
        with open(csv_file, 'r') as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                this_cls = cls(event_id=int(row['EVENT_ID']),
                               fatality_id=int(row['FATALITY_ID']),
                               fatality_time=to_datetime(
                                   row['FAT_YEARMONTH'], row['FAT_DAY']),
                               fatality_type='direct'
                               if row['FATALITY_TYPE'] == 'D' else 'indirect',
                               fatality_age=int(row['FATALITY_AGE'])
                               if len(row['FATALITY_AGE']) else None,
                               fatality_sex=row['FATALITY_SEX']
                               if len(row['FATALITY_SEX']) else None,
                               fatality_location=row['FATALITY_LOCATION'])
                cls_list.append(this_cls)

        return cls_list
