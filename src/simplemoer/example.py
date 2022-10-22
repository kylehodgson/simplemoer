#!/usr/bin/env pythob
from client import WattTime

wt=WattTime()
index=wt.get_index()
print(f"index: {index}")
