from random import randint


class Character:
    def __init__(self, health, dmg):
        self.max_health = int(health)
        self.health = int(health)
        self.dmg = dmg
        # Skill Id, Explanation, Cooldown count, Cooldown
        self.skill = []
        # effect, explanation
        self.passive_skill = [0, '']
        self.alive = True

    def get_name(self):
        return "Character"

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def get_max_health(self):
        return self.max_health

    def set_max_health(self):
        self.health = self.max_health

    def get_dmg(self):
        return self.dmg

    def get_alive(self):
        return self.alive

    def set_alive(self):
        self.alive = True

    def get_skill(self):
        return "Skill: " + self.skill[1]

    def get_passive_skill(self):
        return "Passive: " + self.passive_skill[1] + "\n"

    def __str__(self):
        return self.get_name() + " -> " + "Stats: " + str(self.max_health) + "HP and " + str(self.dmg) + "DMG"

    def set_die(self):
        self.alive = False

    def deal_damage(self, enemy, dmg):
        real_dmg = dmg + (self.passive_skill[0] if self.passive_skill[0] > 0 else 0)
        enemy.take_damage(real_dmg)
        return real_dmg

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

    def set_cooldown(self):
        self.skill[2] = self.skill[3]

    def get_cooldown(self):
        return self.skill[2]

    def update_cooldown(self):
        if self.get_cooldown() > 0:
            self.skill[2] -= 1

    def reset_cooldown(self):
        self.skill[2] = 0

    def heal_after_turn(self):
        health_after_level = self.health + (1/4) * self.max_health
        if self.health < self.max_health:
            if health_after_level <= self.max_health:
                self.health += (1/4) * self.max_health
            else:
                self.health = self.max_health


class Bookworm(Character):
    def __init__(self):
        super().__init__(health=25, dmg=9)
        self.skill = ['Resurrect', 'Revives one player(4 rounds)', 0, 4]

    def get_name(self):
        return "Bookworm"

    def __str__(self):
        return super().__str__() + '\n\t' + self.get_skill()


class Worker(Character):
    def __init__(self):
        super().__init__(health=40, dmg=10)
        self.skill = ['Amp. DMG', '1.5 * (DMG + DMG roll) damage to one enemy (3 rounds)', 0, 3]

    def get_name(self):
        return "Worker"

    def __str__(self):
        return super().__str__() + '\n\t' + self.get_skill()


class Procrastinator(Character):
    def __init__(self):
        super().__init__(health=30, dmg=6)
        self.passive_skill = [1, 'Adds +1 DMG each round. Resets at the beginning of each level.']
        # Skill Id, Explanation, Cooldown count, Cooldown, Uses
        self.skill = ['AOE', 'DMG + DMG roll + stage level to all the enemies \n\t after the third round /'
                             'of each stage and once per stage.', 3, 3, 1]

    def get_skill_uses(self):
        return self.skill[4]

    def skill_uses_depleted(self):
        self.skill[4] = 0

    def reset_skill_uses(self):
        self.skill[4] = 1

    def reset_passive_skill(self):
        self.passive_skill[0] = 1

    def update_passive_skill(self):
        self.passive_skill[0] += 1

    def reset_cooldown(self):
        self.skill[2] = 3

    def get_name(self):
        return "Procrastinator"

    def __str__(self):
        return super().__str__() + '\n\t' + self.get_passive_skill() + self.get_skill()


class Whatsapper(Character):
    def __init__(self):
        super().__init__(health=20, dmg=6)
        self.skill = ['Heal', 'Heals 2*DMG to one player (3 rounds)', 0, 3]

    def get_name(self):
        return "Whatsapper"

    def __str__(self):
        return super().__str__() + '\n\t' + self.get_skill()
