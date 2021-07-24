from engine import *


class Player:
    class State(enum.Flag):
        IDLE = enum.auto()
        WALKING = enum.auto()
        ATTACKING = enum.auto()

    def __init__(self):
        self.x = width() / 2
        self.y = height() / 2

        self.state = Player.State.IDLE
        self.frame = 0
        self.frame2 = 0 # for swinging arm

    def render(self, look: list):
        img = Player.render.textures

        if len(img) == 0:
            img['leg']  = load_image('textures/player/leg.png')
            img['body'] = load_image('textures/player/body.png')
            img['arm']  = load_image('textures/player/arm.png')
            img['head'] = load_image('textures/player/head.png')
        
        def leg(x: float, y: float, deg: float):
            pushMatrix()
            translate(x, y)
            rotate(deg)
            translate(-img['leg'].width / 2, -img['leg'].height)
            image(img['leg'], 0, 0)
            popMatrix()
        def body(x: float, y: float):
            image(img['body'], x - img['body'].width / 2, y)
        def arm(x: float, y: float, deg: float):
            pushMatrix()
            translate(x, y + img['body'].height)
            rotate(deg)
            translate(-img['arm'].width / 2, -img['arm'].height)
            image(img['arm'], 0, 0)
            popMatrix()
        def head(x: float, y: float, deg: float):                        
            pushMatrix()
            translate(x, y + img['body'].height)
            if abs(deg) > 90:
                scale(-1, 1)
                rotate(-deg + 180)
            else:
                rotate(deg)
            translate(-img['head'].width / 2, 0)
            image(img['head'], 0, 0)
            popMatrix()

        if self.state & Player.State.WALKING:
            self.frame += 0.15
        elif self.state & Player.State.IDLE:
            self.frame %= math.pi
            self.frame += (math.pi - self.frame) * 0.2

        # head angle
        rad = math.atan2(look[1] - (self.y + img['body'].height), look[0] - self.x)
        deg = math.degrees(rad)

        arms = [45 * math.sin(self.frame), 45 * math.sin(-self.frame)]
        if self.state & Player.State.ATTACKING:
            self.frame2 += 0.6
            # swinging arm
            arms[0] = 5 * math.sin(self.frame2) + deg + 90
            # walking arm moves a bit less
            arms[1] *= 0.2

        leg(self.x, self.y, 45 * math.sin(self.frame))
        leg(self.x, self.y, 45 * math.sin(math.pi + self.frame))
        arm(self.x, self.y, arms[1])
        body(self.x, self.y)
        arm(self.x, self.y, arms[0])
        head(self.x, self.y, deg)


Player.render.textures = {}