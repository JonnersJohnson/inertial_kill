
class Particle:
    def __init__(self, p_type, subtype, faction, x, y, velx, vely):
        self.p_type = p_type
        self.subtype = subtype
        self.faction = faction
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.dv = 10.0
        self.missiles = 50
        self.req_dv = 0.0
        if self.p_type == "ship":
            self.defence = 100
            self.mdef = 4
            self.boost_v = 3


# Initial conditions
ship1 = Particle("ship", "destroyer", "USA", 50, 200, 1, 4)
ship2 = Particle("ship", "destroyer", "USSR", 600, 200, -1, 3)
particles = [ship1, ship2]




