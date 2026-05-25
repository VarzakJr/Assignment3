# util.py (add this)
import util

def apply_step_teleport(x, y, dx, dy):
    """Apply one displacement step under 'teleport to a' rules."""
    nx = x + dx
    ny = y + dy
    if nx < 0 or nx >= util.WIDTH or ny < 0 or ny >= util.HEIGHT:
        # teleport to 'a', which we take as (0,0)
        return 0, 0
    return nx, ny

def compose_teleport(a, b):
    """
    Operation * for Task 1.b.
    Interpret action indices as single-step displacements, then
    simulate from a starting at 'a' (0,0).
    """
    ax, ay = util.idx_to_disp(a)
    bx, by = util.idx_to_disp(b)

    # First apply a from (0,0)
    x, y = apply_step_teleport(0, 0, ax, ay)
    # Then apply b from that new position
    x, y = apply_step_teleport(x, y, bx, by)
    return util.disp_to_idx(x, y)