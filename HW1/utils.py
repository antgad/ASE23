import NUM
import SYM
import math

Seed=937162211

def rand(lo=0,hi=1):
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647 

function rnd(n, nPlaces) --> num. return `n` rounded to `nPlaces`
  local mult = 10^(nPlaces or 3)
  return math.floor(n * mult + 0.5) / mult

def rnd(n,nPlaces=3):
    mult = pow(10,nPlaces)
    return math.floor(n*mult+0.5)
