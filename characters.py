from random import randint

class Character:
    def __init__(self, health, dmg):
        self.max_health = health
        self.health = health
        self.dmg = dmg
        # effect, explanation, cooldown count, cooldown
        self.skill = []
        # effect, explanation
        self.passive_skill = [0, '']
        self.alive = True

    def get_name(self):
        return "Character"

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_dmg(self):
        return self.dmg

    def get_alive(self):
        return self.alive

    def get_skill(self):
        return "SKill: " + self.skill[1]

    def get_passive_skill(self):
        return "Passsive: " + self.passive_skill[1] + "\n"

    def __str__(self):
        return self.get_name() + " -> " + "Stats: " + self.get_health() + "HP and " + self.dmg() + "DMG\n"

    def set_die(self):
        self.alive = False

    def deal_damage(self, enemy, dmg):
        enemy.takeDamage(dmg * (self.passive_skill[0] if self.passive_skill[0] > 0 else 0))

    def take_damage(self, dmg):
        if (self.get_health() - dmg) > 0:
            self.health -= dmg
        else:
            self.set_die()

    def damage_roll(self):
        return randint(1, self.dmg)

    def attack(self, target):
        self.deal_damage(target, self.damage_roll())

    def set_cooldown(self):
        self.skill[2] = self.skill[3]

    def update_cooldown(self):
        for skill in self.skill:
            if skill[2] > 0:
                skill[2] -= 1

