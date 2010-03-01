# -*- coding: utf-8 -*-
import pygame
import player
import pipe
import placeholder


class MouseState:
    "Es un estado de comportamiento del mouse."

    def __init__(self, mouse):
        self.mouse = mouse
        print "MOUSE", self

    def update(self):
        pass

    def on_click(self, x, y):
        pass

class PointToWorkAt(MouseState):
    "Está por indicarle una coordenada a un trabajador."

    def __init__(self, mouse, player):
        MouseState.__init__(self, mouse)
        self.player = player
        self.mouse.set_frame("normal")

    def update(self):
        sprite = self.mouse.get_placeholder_over_mouse()

        if sprite:
            self.mouse.set_frame("over")
        else:
            self.mouse.set_frame("normal")


    def on_click(self, x, y):
        placeholder = self.mouse.get_placeholder_over_mouse()

        if placeholder:
            pipe = self.player.state.pipe
            self.player.walk_and_work_in_a_placeholder(pipe, placeholder, x, y)
        else:
            pipe = self.player.state.pipe

            dist = abs(y - self.player.rect.bottom)

            if dist < 26:
                self.player.walk_to_leave_pipe_here(pipe, x, y)
            else:
                self.player.walk_to_with_piece(pipe, x, y)

        self.mouse.change_state(Normal(self.mouse))

class PointAt(MouseState):
    "Está por indicarle una coordenada a un trabajador."

    def __init__(self, mouse, player):
        MouseState.__init__(self, mouse)
        self.player = player
        self.mouse.set_frame("normal")

    def update(self):
        sprite = self.mouse.get_pipe_over_mouse()

        if sprite:
            self.mouse.set_frame("over")
        else:
            self.mouse.set_frame("normal")

    def on_click(self, x, y):
        sprite = self.mouse.get_pipe_over_mouse()

        if sprite:
            if sprite.are_in_a_placeholder:
                placeholder = sprite.get_placeholder()
                self.player.walk_to_remove_a_pipe_from_placeholder(sprite, placeholder, x, y)
            else:
                self.player.walk_and_take_the_pipe(sprite, x, y)
        else:
            self.player.walk_to(x, y)

        self.mouse.change_state(Normal(self.mouse))

            
class Normal(MouseState):
    "Representa el mouse cuando explora la escena y no ha pulsado."

    def __init__(self, mouse):
        MouseState.__init__(self, mouse)
        self.mouse.set_frame("normal")

    def update(self):
        if self.mouse.visible:
            sprite = self.mouse.get_player_over_mouse()

            if sprite and sprite.can_receive_new_jobs():
                self.mouse.set_frame("over")
            else:
                self.mouse.set_frame("normal")

    def on_click(self, x, y):
        sprite = self.mouse.get_player_over_mouse()

        if sprite and sprite.can_receive_new_jobs():
            if sprite.has_a_pipe_in_hands:
                self.mouse.change_state(PointToWorkAt(self.mouse, sprite))
            else:
                self.mouse.change_state(PointAt(self.mouse, sprite))
