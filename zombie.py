import random
import math
import game_framework
import game_world

from pico2d import *

from state_machine import StateMachine, Die

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0
FRAMES_PER_ACTION_DEAD = 12.0

animation_names = ['Walk','Dead']
class Dead:
    @staticmethod
    def enter(zombie, e):
        pass

    @staticmethod
    def exit(zombie, e):
        pass

    @staticmethod
    def do(zombie):
        zombie.frame = (zombie.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_DEAD


    @staticmethod
    def draw(zombie):
        if zombie.dir < 0:
            Zombie.images['Dead'][int(zombie.frame)].composite_draw(0, 'h', zombie.x, zombie.y, 200, 200)
        else:
            Zombie.images['Dead'][int(zombie.frame)].draw(zombie.x, zombie.y, 200, 200)

        if int(zombie.frame) == FRAMES_PER_ACTION_DEAD - 1:
            game_world.remove_object(zombie)


class Walk:
    @staticmethod
    def enter(zombie, e):
        pass

    @staticmethod
    def exit(zombie, e):
        pass

    @staticmethod
    def do(zombie):
        zombie.frame = (zombie.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        zombie.x += RUN_SPEED_PPS * zombie.dir * game_framework.frame_time
        if zombie.x > 1600:
            zombie.dir = -1
        elif zombie.x < 800:
            zombie.dir = 1
        zombie.x = clamp(800, zombie.x, 1600)

    @staticmethod
    def draw(zombie):
        if zombie.dir < 0:
            Zombie.images['Walk'][int(zombie.frame)].composite_draw(0, 'h', zombie.x, zombie.y, 200, 200)
        else:
            Zombie.images['Walk'][int(zombie.frame)].draw(zombie.x, zombie.y, 200, 200)









class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                if name == 'Walk':
                    max_frame = 11
                elif name == 'Dead':
                    max_frame = 13
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, max_frame)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.heath = 2
        self.state_machine = StateMachine(self)
        self.state_machine.start(Walk)
        self.state_machine.set_transitions(
            {
                Walk : { Die : Dead },
                Dead : {}
            }
        )



    def update(self):
        self.state_machine.update()



    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 80, self.y - 100, self.x + 80, self.y + 100

    def handle_collision(self, group, other):
        if group == 'zombie:shot_ball':
            if self.heath > 0:
                self.heath -= 1
            else:
                self.state_machine.add_event(('DIE',0))
