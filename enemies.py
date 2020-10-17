
class Enermies:
    def __init__(self, health, dmg):
        self.health = health
        self.dmg = dmg
        self.skill = []
        self.alive = True

    def getName(self):
        return "Enemy"

    def __str__(self):
        return self.getName() + " -> " + " Stats: " + str(self.health) + "HP and " + str(self.damage) + "DM"

    def dealDamage(self, character, dmg):
        character.takeDamage(dmg)

    def takeDamage(self, dmg):
        self.health -= dmg

    def attack(self, target):
        skill = self.skill[2]
        dmg = skill + self.dmg
        self.dealDamage(target, dmg)

    def getHealth(self):
        return self.health

    def die(self):
        self.alive = False

    def getAlive(self):
        return self.alive

