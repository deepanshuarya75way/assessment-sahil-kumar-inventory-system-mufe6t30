from datetime import datetime, date, timedelta
import math
from math import ceil

def forecast(demand):
  if len(demand) < 14 or sum(x>0 for x in demand) < 3:
    return 0, "uncertain"

  nz = [x for x in demand if x]
  if len(nz) / len(demand) <0.5:
    return sum(nz) / len(demand), "medium"
  return sum(demand[-7:]) / min(7, len(demand)), "high"


def stockout(stock, daily):
  if stock<=0 or daily<=0:
    return None
  return date.today() + timedelta(days = math.ceil(stock/daily))

def reorder(stock , daily, lead = 7, safety = 3):
    
  return max(0, math.ceil(daily*(lead+safety)-stock))