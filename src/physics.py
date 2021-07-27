class Aabb:
    """Axis aligned bound box, where x, y are at its center"""
    def __init__(self, x, y, w, h):
        """x, y are coordinates at this bbox's center"""
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def intersects(self, other) -> bool:
        if self.w == 0 or self.h == 0: return False
        if other.w == 0 or other.h == 0: return False

        x = abs(self.x - other.x) * 2 < (self.w + other.w)
        y = abs(self.y - other.y) * 2 < (self.h + other.h)
        
        return x and y