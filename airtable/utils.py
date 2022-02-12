#!/usr/bin/env python3
# 02/11/22
# utils.py
# rudy@sprints

def require(*conditions, error=ValueError()):
    if not all(conditions):
        raise error
