# util.py
from secrets import randbelow  # allowed by the assignment rules

# Grid dimensions for Task 1.a (wrap-around)
WIDTH = 3
HEIGHT = 2

def idx_to_disp(g):
    dx = g // HEIGHT  # 0..2
    dy = g % HEIGHT   # 0..1
    return dx, dy

def disp_to_idx(dx, dy):
    return dx * HEIGHT + dy  # 0..5

def compose_wrap(a, b):
    """Operation * for Task 1.a (wrap-around grid)."""
    ax, ay = idx_to_disp(a)
    bx, by = idx_to_disp(b)
    cx = (ax + bx) % WIDTH
    cy = (ay + by) % HEIGHT
    return disp_to_idx(cx, cy)

def identity_wrap():
    return 0  # (0,0) displacement

def inverse_wrap(a):
    """Inverse in the group of Task 1.a."""
    ax, ay = idx_to_disp(a)
    dx = (-ax) % WIDTH
    dy = (-ay) % HEIGHT
    return disp_to_idx(dx, dy)

def random_action():
    return randbelow(WIDTH * HEIGHT)  # uniform in G