#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 09:04:18 2023

@author: mike
"""
from datetime import date

from pydantic import BaseModel

#########################################
### Models


class Plan(BaseModel):
    """ """

    plan_id: str
    plan_name: str
    commencement_date: date
    plan_authority: str
