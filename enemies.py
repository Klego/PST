from random import randint


class Enemies:
    def __init__(self, health, dmg):
        self.health = health
        self.dmg = dmg
        # name, damage, explanation
        self.skill = []
        self.alive = True

    def get_name(self):
        return "Enemy"

    def get_health(self):
        return self.health

    def get_alive(self):
        return self.alive

    def set_die(self):
        self.alive = False

    def __str__(self):
        return self.get_name() + ": " + " Stats: " + str(self.health) + "HP and " + str(self.dmg) + "DMG\n"

    def deal_damage(self, character, dmg):
        character.take_damage(dmg)
        return dmg

    def take_damage(self, dmg):
        if (self.get_health() - dmg) > 0:
            self.health -= dmg
        else:
            self.set_die()

    def damage_roll(self):
        return randint(1, self.dmg)

    def attack(self, target):
        real_damage = self.deal_damage(target, self.damage_roll())
        return real_damage


class PartialExam(Enemies):
    def __init__(self):
        super().__init__(health=20, dmg=6)

    def get_name(self):
        return "Partial Exam"


class FinalExam(Enemies):
    def __init__(self):
        super().__init__(health=40, dmg=12)
        self.skill = ['From 4th to beyond', 0, 'It only appears beyond 4th floor']

    def get_name(self):
        return "Final Exam"


class TheoreticalClass(Enemies):
    def __init__(self, level):
        super().__init__(health=8, dmg=4)
        self.level = level
        self.skill = ['Lucky DMG', level, 'Add to the damage the floor on which it appears']

    def attack(self, target):
        dmg = self.skill[1] + self.damage_roll()
        real_damage = self.deal_damage(target, dmg)
        return real_damage

    def get_name(self):
        return "Theoretical Class"


class Teacher(Enemies):
    def __init__(self):
        super().__init__(health=15, dmg=7)
        self.skill = ['Double Max Output', 7, 'If the damage roll is 7, it adds the damage of this skill']

    def attack(self, target):
        roll = self.damage_roll()
        if roll == 7:
            dmg = self.skill[1] + roll
        else:
            dmg = self.damage_roll()

        real_damage = self.deal_damage(target, dmg)
        return real_damage

    def get_name(self):
        return "Teacher"
