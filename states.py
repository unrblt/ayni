# -*- coding: utf-8 -*-

class State:
    "Representa un estado del personaje del juego."

    def __init__(self, player):
        self.player = player
        #print "pasando al estado", self.__class__.__name__

    def update(self):
        pass


class Stand(State):
    "El personaje esta en estado 'parado' o 'esperando'"

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation("stand")


class StandWithPiece(State):
    "El personaje esta en estado 'parado' o 'esperando'"

    def __init__(self, player, pipe):
        self.pipe = pipe
        State.__init__(self, player)
        self.player.set_animation("stand_moving")

    def on_click(self, x, y):
        if self.player.collides(x, y):
            self.player.change_state(Wait(self.player))


class Walk(State):
    "Se mueve a la posición que le indiquen."

    def __init__(self, player, x, y):
        State.__init__(self, player)
        # a 'y' no le da bola...
        self.to_x = x
        #self.player.messages.remove_last_balloon_sprite()
        self.player.set_animation("walk")

        if player.rect.centerx < x:
            self.dx = 3
            self.player.flip = True
        else:
            self.dx = -3
            self.player.flip = False

    def update(self):
        # Verifica obstaculos
        x, y = self.player.rect.centerx + self.dx, self.player.rect.y + 20

        if not self._closer():
            self.player.rect.x += self.dx
        else:
            self.player.change_state(Stand(self.player))

        '''
        if self.player.can_move_to(x, y):
            if not self._closer():
                self.player.rect.x += self.dx
            else:
                self.player.say("listo...")
                self.player.change_state(Stand(self.player))
        else:
            self.player.change_state(Refuse(self.player))
        '''

    def _closer(self):
        "Indica si está muy, muy cerca de el lugar a donde ir."
        return abs(self.player.rect.centerx - self.to_x) < 3


class Refuse(State):
    "Aguarda unos instantes y regresa al estado Stand."

    def __init__(self, player):
        State.__init__(self, player)
        self.player.set_animation('boo')
        self.delay = 50
        self.player.say(u"nah, no voy ahí.")

    def update(self):
        self.delay -= 1

        if self.delay < 0:
            self.player.change_state(Stand(self.player))

class Wait(State):
    "El personaje espera que le digan que hacer."

    def __init__(self, player):
        State.__init__(self, player)
        player.say("Decime...")
        player.set_animation('wait')

    def on_click(self, x, y):
        "Intenta ir al punto indicado o advierte si lo re-seleccionan."

        # Si lo seleccionan de nuevo se queja...
        if self.player.collides(x, y):
            self._repeat_instructions()
            return

        # Va a donde le indiquen.
        if self.player.can_move_to(x, y):
            #self.player.say(u"ahí voy...")
            self.player.change_state(Walk(self.player, x, y))
        else:
            # Si le dicen que se tire, no es boludo...
            self.player.change_state(Refuse(self.player))


    def _repeat_instructions(self):
        "Repite al usuario que le indique el camino."
        messages = [
                u"si, ok, ¿que hago?",
                u"indicame el camino...",
                u"¿a donde?",
                ]
        any_text = random.choice(messages)
        self.player.say(any_text)
