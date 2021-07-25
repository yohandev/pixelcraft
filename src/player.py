from engine import *
from physics import Aabb


class Player:
    class State(enum.Flag):
        IDLE = enum.auto()
        WALKING = enum.auto()
        ATTACKING = enum.auto()

    def __init__(self):
        self.x = 0
        self.y = 0

        self.state = Player.State.IDLE
        self.frame = 0
        self.frame2 = 0 # for swinging arm

    def aabb(self): return Aabb(self.x, self.y, 0.75, 2)

    def render(self, x: float, y: float, mx: float, my: float):
        img = Player.render.textures

        if len(img) == 0:
            img['leg']  = load_image('textures/player/leg.png')
            img['body'] = load_image('textures/player/body.png')
            img['arm']  = load_image('textures/player/arm.png')
            img['head'] = load_image('textures/player/head.png')
        
        def leg(x: float, y: float, deg: float):
            push_matrix()
            translate(x, y)
            rotate(deg)
            translate(-img['leg'].width / 2, -img['leg'].height)
            image(img['leg'], 0, 0)
            pop_matrix()
        def body(x: float, y: float):
            image(img['body'], x - img['body'].width / 2, y)
        def arm(x: float, y: float, deg: float):
            push_matrix()
            translate(x, y + img['body'].height)
            rotate(deg)
            translate(-img['arm'].width / 2, -img['arm'].height)
            image(img['arm'], 0, 0)
            pop_matrix()
        def head(x: float, y: float, deg: float):                        
            push_matrix()
            translate(x, y + img['body'].height)
            if abs(deg) > 90:
                scale(-1, 1)
                rotate(-deg + 180)
            else:
                rotate(deg)
            translate(-img['head'].width / 2, 0)
            image(img['head'], 0, 0)
            pop_matrix()

        if self.state & Player.State.WALKING:
            self.frame += 0.15
        elif self.state & Player.State.IDLE:
            self.frame %= math.pi
            self.frame += (math.pi - self.frame) * 0.2

        # head angle
        rad = math.atan2(my - (y + img['body'].height), mx - x)
        deg = math.degrees(rad)

        arms = [45 * math.sin(self.frame), 45 * math.sin(-self.frame)]
        if self.state & Player.State.ATTACKING:
            self.frame2 += 0.6
            # swinging arm
            arms[0] = 5 * math.sin(self.frame2) + deg + 90
            # walking arm moves a bit less
            arms[1] *= 0.2

        leg(x, y, 45 * math.sin(self.frame))
        leg(x, y, 45 * math.sin(math.pi + self.frame))
        arm(x, y, arms[1])
        body(x, y)
        arm(x, y, arms[0])
        head(x, y, deg)


Player.render.textures = {}