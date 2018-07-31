
# list of shapes

# Here list all the possible shapes of 21 tiles
# using + to represent a square

shapeSet = [
# type 0: O1
#  
# +
#
   [[(0, 0)], 
    [(0, 0)], 
    [(0, 0)], 
    [(0, 0)],
    [(0, 0)],
    [(0, 0)],
    [(0, 0)],
    [(0, 0)]],

# type 1: I2
# 
# ++
#
   [[(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1)]],

# type 2: I3
# 
# +++
#
   [[(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2)]],

# type 3: L3
# 
# +
# ++
#
   [[(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)]],

# type 4: O4
#
# ++
# ++
#
   [[(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]],

# type 5: Z4
#
#  +
# ++
# +
#
   [[(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (2, 0)],
    [(0, 1), (0, 2), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (0, 2), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)]],

# type 6: T4
#
#  + 
# +++
#
   [[(0, 0), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)]],

# type 7: I4
#
# ++++
#
   [[(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3)]],

# type 8: L4
# 
# +
# +
# ++
# 
   [[(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 2)],
    [(0, 1), (1, 1), (2, 0), (2, 1)]],

# type 9: U5
# 
# + +
# +++
# 
   [[(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]],

# type 10: P5
# 
# +
# ++
# ++
# 
   [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]],

# type 11: I5
#
# +++++
#
   [[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]],

# type 12: T5
# 
#  +
#  +
# +++
# 
   [[(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)]],

# type 13: Z_5
#
# ++
#  +++
#
   [[(0, 1), (1, 0), (1, 1), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)],
    [(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
    [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)],
    [(0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]],

# type 14: Z5
#
# ++
#  +
#  ++
#
   [[(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1)]],

# type 15: L5
#
# +
# +
# +++
#
   [[(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]],

# type 16: L_5
#
# +
# ++++
#
   [[(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],
    [(0, 1), (1, 1), (2, 1), (3, 0), (3, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
    [(0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]],

# type 17: Y5
# 
# +
# ++
# +
# +
# 
   [[(0, 0), (0, 1), (0, 2), (0, 3), (1, 2)],
    [(0, 1), (1, 1), (2, 0), (2, 1), (3, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)],
    [(0, 0), (1, 0), (1, 1), (2, 0), (3, 0)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (1, 3)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)]],

# type 18: F5
#
#  +
# ++
#  ++
#
   [[(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)],
    [(0, 2), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 1), (1, 1), (1, 2), (2, 0), (2, 1)]],

# type 19: W5
#
# +
# ++
#  ++
#
   [[(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
    [(0, 2), (1, 1), (1, 2), (2, 0), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
    [(0, 2), (1, 1), (1, 2), (2, 0), (2, 1)]],

# type 20: X5
#
#  +
# +++
#  +
#
   [[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]],
]

# corners of the corresponding shape

cornerSet = [
# type 0: O1
   [[(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)], 
    [(-1, -1), (-1, 1), (1, -1), (1, 1)]],

# type 1: I2
   [[(-1, 1), (-1, -1), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (1, -1), (1, 2)],
    [(-1, 1), (-1, -1), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (1, -1), (1, 2)],
    [(-1, 1), (-1, -1), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (1, -1), (1, 2)],
    [(-1, 1), (-1, -1), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (1, -1), (1, 2)]],

# type 2: I3
   [[(-1, 1), (-1, -1), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (1, -1), (1, 3)],
    [(-1, 1), (-1, -1), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (1, -1), (1, 3)],
    [(-1, 1), (-1, -1), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (1, -1), (1, 3)],
    [(-1, 1), (-1, -1), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (1, -1), (1, 3)]],

# type 3: L3
   [[(-1, 2), (1, 2), (2, 1), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, 0), (1, -1), (-1, -1)],
    [(-1, 0), (-1, 2), (2, 2), (2, -1), (0, -1)],
    [(-1, 1), (0, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 1), (0, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (1, 2), (2, 1), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, 0), (1, -1), (-1, -1)],
    [(-1, 0), (-1, 2), (2, 2), (2, -1), (0, -1)]],

# type 4: O4
   [[(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)],
    [(-1, 2), (2, 2), (2, -1), (-1, -1)]],

# type 5: Z4
   [[(-1, 2), (0, 3), (2, 3), (2, 0), (1, -1), (-1, -1)],
    [(-1, 0), (-1, 2), (2, 2), (3, 1), (3, -1), (0, -1)],
    [(-1, 2), (0, 3), (2, 3), (2, 0), (1, -1), (-1, -1)],
    [(-1, 0), (-1, 2), (2, 2), (3, 1), (3, -1), (0, -1)],
    [(-1, 0), (-1, 3), (1, 3), (2, 2), (2, -1), (0, -1)],
    [(-1, 1), (0, 2), (3, 2), (3, 0), (2, -1), (-1, -1)],
    [(-1, 0), (-1, 3), (1, 3), (2, 2), (2, -1), (0, -1)],
    [(-1, 1), (0, 2), (3, 2), (3, 0), (2, -1), (-1, -1)]],

# type 6: T4
   [[(-1, 1), (0, 2), (2, 2), (3, 1), (3, -1), (-1, -1)],
    [(-1, 3), (1, 3), (2, 2), (2, 0), (1, -1), (-1, -1)],
    [(-1, 2), (3, 2), (3, 0), (2, -1), (0, -1), (-1, 0)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (2, -1), (0, -1)],
    [(-1, 1), (0, 2), (2, 2), (3, 1), (3, -1), (-1, -1)],
    [(-1, 3), (1, 3), (2, 2), (2, 0), (1, -1), (-1, -1)],
    [(-1, 2), (3, 2), (3, 0), (2, -1), (0, -1), (-1, 0)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (2, -1), (0, -1)]],

# type 7: I4
   [[(-1, 1), (-1, -1), (4, 1), (4, -1)],
    [(-1, -1), (-1, 4), (1, -1), (1, 4)],
    [(-1, 1), (-1, -1), (4, 1), (4, -1)],
    [(-1, -1), (-1, 4), (1, -1), (1, 4)],
    [(-1, 1), (-1, -1), (4, 1), (4, -1)],
    [(-1, -1), (-1, 4), (1, -1), (1, 4)],
    [(-1, 1), (-1, -1), (4, 1), (4, -1)],
    [(-1, -1), (-1, 4), (1, -1), (1, 4)]],

# type 8: L4
   [[(-1, -1), (-1, 3), (1, 3), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (3, 2), (3, 0), (1, -1)],
    [(-1, 1), (-1, 3), (2, 3), (2, -1), (0, -1)],
    [(-1, -1), (-1, 1), (1, 2), (3, 2), (3, -1)],
    [(-1, -1), (-1, 1), (0, 3), (2, 3), (2, -1)],
    [(-1, -1), (-1, 2), (1, 2), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (2, 3), (2, 1), (1, -1)],
    [(-1, 0), (-1, 2), (3, 2), (3, -1), (1, -1)]],

# type 9: U5
   [[(-1, -1), (-1, 2), (1, 2), (3, 2), (3, -1)],
    [(-1, -1), (-1, 3), (2, 3), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (3, 2), (3, -1), (1, -1)],
    [(-1, -1), (-1, 1), (-1, 3), (2, 3), (2, -1)],
    [(-1, -1), (-1, 2), (1, 2), (3, 2), (3, -1)],
    [(-1, -1), (-1, 3), (2, 3), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (3, 2), (3, -1), (1, -1)],
    [(-1, -1), (-1, 1), (-1, 3), (2, 3), (2, -1)]],

# type 10: P5
   [[(-1, -1), (-1, 3), (1, 3), (2, 2), (2, -1)],
    [(-1, -1), (-1, 2), (3, 2), (3, 0), (2, -1)],
    [(-1, 0), (-1, 3), (2, 3), (2, -1), (0, -1)],
    [(-1, -1), (-1, 1), (0, 2), (3, 2), (3, -1)],
    [(-1, -1), (-1, 2), (0, 3), (2, 3), (2, -1)],
    [(-1, -1), (-1, 2), (2, 2), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (2, 3), (2, 0), (1, -1)],
    [(-1, 0), (-1, 2), (3, 2), (3, -1), (0, -1)]],

# type 11: I5
   [[(-1, 1), (-1, -1), (5, 1), (5, -1)],
    [(-1, -1), (-1, 5), (1, -1), (1, 5)],
    [(-1, 1), (-1, -1), (5, 1), (5, -1)],
    [(-1, -1), (-1, 5), (1, -1), (1, 5)],
    [(-1, 1), (-1, -1), (5, 1), (5, -1)],
    [(-1, -1), (-1, 5), (1, -1), (1, 5)],
    [(-1, 1), (-1, -1), (5, 1), (5, -1)],
    [(-1, -1), (-1, 5), (1, -1), (1, 5)]],

# type 12: T5
   [[(-1, -1), (-1, 1), (0, 3), (2, 3), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (1, 3), (3, 2), (3, 0), (1, -1)],
    [(-1, 1), (-1, 3), (3, 3), (3, 1), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (1, 3), (3, 3), (3, -1), (1, -1)],
    [(-1, -1), (-1, 1), (0, 3), (2, 3), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (1, 3), (3, 2), (3, 0), (1, -1)],
    [(-1, 1), (-1, 3), (3, 3), (3, 1), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (1, 3), (3, 3), (3, -1), (1, -1)]],

# type 13: Z_5
   [[(-1, 0), (-1, 2), (2, 2), (4, 1), (4, -1), (0, -1)],
    [(-1, -1), (-1, 3), (0, 4), (2, 4), (2, 1), (1, -1)],
    [(-1, 0), (-1, 2), (3, 2), (4, 1), (4, -1), (1, -1)],
    [(-1, -1), (-1, 2), (0, 4), (2, 4), (2, 0), (1, -1)],
    [(-1, -1), (-1, 1), (1, 2), (4, 2), (4, 0), (3, -1)],
    [(-1, 0), (-1, 4), (1, 4), (2, 2), (2, -1), (0, -1)],
    [(-1, -1), (-1, 1), (0, 2), (4, 2), (4, 0), (2, -1)],
    [(-1, 1), (-1, 4), (1, 4), (2, 3), (2, -1), (0, -1)]],

# type 14: Z5
   [[(-1, 1), (-1, 3), (2, 3), (3, 1), (3, -1), (0, -1)],
    [(-1, -1), (-1, 2), (1, 3), (3, 3), (3, 0), (1, -1)],
    [(-1, 1), (-1, 3), (2, 3), (3, 1), (3, -1), (0, -1)],
    [(-1, -1), (-1, 2), (1, 3), (3, 3), (3, 0), (1, -1)],
    [(-1, -1), (-1, 1), (0, 3), (3, 3), (3, 1), (2, -1)],
    [(-1, 0), (-1, 3), (1, 3), (3, 2), (3, -1), (1, -1)],
    [(-1, -1), (-1, 1), (0, 3), (3, 3), (3, 1), (2, -1)],
    [(-1, 0), (-1, 3), (1, 3), (3, 2), (3, -1), (1, -1)]],

# type 15: L5
   [[(-1, -1), (-1, 3), (1, 3), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (3, 3), (3, 1), (1, -1)],
    [(-1, 1), (-1, 3), (3, 3), (3, -1), (1, -1)],
    [(-1, -1), (-1, 1), (1, 3), (3, 3), (3, -1)],
    [(-1, -1), (-1, 1), (1, 3), (3, 3), (3, -1)],
    [(-1, -1), (-1, 3), (1, 3), (3, 1), (3, -1)],
    [(-1, -1), (-1, 3), (3, 3), (3, 1), (1, -1)],
    [(-1, 1), (-1, 3), (3, 3), (3, -1), (1, -1)]],

# type 17: L_5
   [[(-1, -1), (-1, 2), (1, 2), (4, 1), (4, -1)],
    [(-1, -1), (-1, 4), (2, 4), (2, 2), (1, -1)],
    [(-1, 0), (-1, 2), (4, 2), (4, -1) ,(2, -1)],
    [(-1, -1), (-1, 1), (0, 4), (2, 4), (2, -1)],
    [(-1, -1), (-1, 1), (2, 2), (4, 2), (4, -1)],
    [(-1, -1), (-1, 4), (1, 4), (2, 1), (2, -1)],
    [(-1, -1), (-1, 2), (4, 2), (4, 0), (1, -1)],
    [(-1, 2), (-1, 4), (2, 4), (2, -1), (0, -1)]],

# type 18: Y5
   [[(-1, -1), (-1, 4), (1, 4), (2, 3), (2, 1), (1, -1)],
    [(-1, 0), (-1, 2), (4, 2), (4, 0), (3, -1), (1, -1)],
    [(-1, 0), (-1, 2), (0, 4), (2, 4), (2, -1), (0, -1)],
    [(-1, -1), (-1, 1), (0, 2), (2, 2), (4, 1), (4, -1)],
    [(-1, 1), (-1, 3), (0, 4), (2, 4), (2, -1), (0, -1)],
    [(-1, -1), (-1, 1), (1, 2), (3, 2), (4, 1), (4, -1)],
    [(-1, -1), (-1, 4), (1, 4), (2, 2), (2, 0), (1, -1)],
    [(-1, 0), (-1, 2), (4, 2), (4, 0), (2, -1), (0, -1)]],

# type 16: F5
   [[(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 1), (3, -1), (0, -1)],
    [(-1, -1), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (1, -1)],
    [(-1, 1), (-1, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (1, 3), (3, 3), (3, 0), (2, -1), (0, -1)],
    [(-1, -1), (-1, 1), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1)],
    [(-1, 0), (-1, 3), (1, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (3, 3), (3, 1), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, -1), (1, -1)]],

# type 19: W5
   [[(-1, 0), (-1, 3), (1, 3), (2, 2), (3, 1), (3, -1), (0, -1)],
    [(-1, -1), (-1, 2), (0, 3), (3, 3), (3, 1), (2, 0), (1, -1)],
    [(-1, 1), (-1, 3), (2, 3), (3, 2), (3, -1), (1, -1), (0, 0)],
    [(-1, -1), (-1, 1), (0, 2), (1, 3), (3, 3), (3, 0), (2, -1)],
    [(-1, -1), (-1, 1), (0, 2), (1, 3), (3, 3), (3, 0), (2, -1)],
    [(-1, 0), (-1, 3), (1, 3), (2, 2), (3, 1), (3, -1), (0, -1)],
    [(-1, -1), (-1, 2), (0, 3), (3, 3), (3, 1), (2, 0), (1, -1)],
    [(-1, 1), (-1, 3), (2, 3), (3, 2), (3, -1), (1, -1), (0, 0)]],

# type 20: X5
   [[(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)],
    [(-1, 0), (-1, 2), (0, 3), (2, 3), (3, 2), (3, 0), (2, -1), (0, -1)]]

]

# size of each tile

tileSizes = [1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

# the most time for a tile to be rotated

tileMaxRotation = [1, 2, 2, 4, 1, 2, 4, 2, 4, 4, 4, 2, 4, 4, 2, 4, 4, 4, 4, 4, 1]

# ascii for each color

colorAscii = [9946, 9930, 9947]