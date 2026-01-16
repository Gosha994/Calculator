def bounce(object_, dx, dy, delta_time):
    if dx != object_.dx:
        object_.center_x += (dx - object_.dx) * delta_time
        object_.dx *= -1
    if dy != object_.dy:
        object_.center_y += (dy - object_.dy) * delta_time
        object_.dy *= -1
