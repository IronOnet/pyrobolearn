#!/usr/bin/env python
"""Provide the Pepper robotic platform.
"""

import os

from pyrobolearn.robots.wheeled_robot import WheeledRobot
from pyrobolearn.robots.manipulator import BiManipulatorRobot
from pyrobolearn.robots.sensors.camera import CameraSensor


class Pepper(WheeledRobot, BiManipulatorRobot):
    r"""Pepper robot.

    The Pepper robot is a robot from the Aldebaran company.

    Note that in the URDF, the continuous joints were replace by revolute joints. Be careful, that the limit values
    for these joints are probably not correct.

    For more information:
        [1] http://doc.aldebaran.com/2-0/home_juliette.html
    """

    def __init__(self,
                 simulator,
                 position=(0, 0, 0.9),
                 orientation=(0, 0, 0, 1),
                 fixed_base=False,
                 scaling=1.,
                 urdf=os.path.dirname(__file__) + '/urdfs/pepper/pepper.urdf'):
        # check parameters
        if position is None:
            position = (0., 0., 0.9)
        if len(position) == 2:  # assume x, y are given
            position = tuple(position) + (0.9,)
        if orientation is None:
            orientation = (0, 0, 0, 1)
        if fixed_base is None:
            fixed_base = False

        super(Pepper, self).__init__(simulator, urdf, position, orientation, fixed_base)
        self.name = 'pepper'

        # 2D Camera sensor
        # From [1]: "Two identical video cameras are located in the forehead. They provide a resolution up to
        # 2560x1080 at 5 frames per second. VFOV = 44.30 deg, HFOV= 57.20 deg, focus = [30cm, infinity]

        # Note that we divide width and height by 4 (otherwise the simulator is pretty slow)
        self.camera_top = CameraSensor(self.sim, self.id, 4, width=2560 / 4, height=1080 / 4, fovy=44.30,
                                       near=0.3, far=100, refresh_rate=60)
        self.camera_bottom = CameraSensor(self.sim, self.id, 9, width=2560 / 4, height=1080 / 4, fovy=44.30,
                                          near=0.3, far=100, refresh_rate=60)

        # 3D camera sensor
        # From [1]: "One 3D camera is located in the forehead. It provides image resolution up to 320x240 at
        # 20 frames per second. One ASUS Xtion 3D sensor is located behind the eyes. VFOV = 45 deg, HFOV = 58 deg,
        # focus = [80cm, 3.5m]."
        self.camera_depth = CameraSensor(self.sim, self.id, 6, width=320, height=240, fovy=45, near=0.3, far=3.5,
                                         refresh_rate=120)

        self.cameras = [self.camera_top, self.camera_bottom, self.camera_depth]


# Test
if __name__ == "__main__":
    from itertools import count
    from pyrobolearn.simulators import BulletSim
    from pyrobolearn.worlds import BasicWorld

    # Create simulator
    sim = BulletSim()

    # create world
    world = BasicWorld(sim)

    # create robot
    robot = Pepper(sim)

    # print information about the robot
    robot.print_info()

    # Position control using sliders
    # robot.add_joint_slider()

    # run simulator
    for i in count():
        # robot.update_joint_slider()
        if i % 20 == 0:
            robot.camera_top.get_rgb_image()
        world.step(sleep_dt=1./240)