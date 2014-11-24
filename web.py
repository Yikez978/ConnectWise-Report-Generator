import random,PIL.Image as I
from math import sin, cos, pi


s=850
def chaos(n,p,r,l):
    i=I.new('RGB',(s,s));x,y=p
    for j in range(n):w,z=random.choice(l);w*=(1-r);z*=(1-r);x,y=x*r+w,y*r+z;i.load()[x,s-y]=s,s,s
    i.show()

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

points = [(425+s*cos(a)/2, 425+s*sin(a)/2) for a in drange(.0, 2*pi, pi/2)]
chaos(1000000, (425, 425), .1, points)