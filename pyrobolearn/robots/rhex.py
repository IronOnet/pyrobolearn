#!/usr/bin/env python
"""Provide the Rhex robotic platform.
"""

import os
import numpy as np

from pyrobolearn.robots.legged_robot import HexapodRobot


# TODO add inertial tags
class Rhex(HexapodRobot):
    r"""Rhex Hexapod robot

    "RHex is a bio-inspired, hexapedal robot designed for locomotion in rough terrain." [1]
    It was created by researchers at the University of Michigan and McGill University.

    References:
        [1] https://robots.ieee.org/robots/rhex/
        [2] https://www.rhex.web.tr/
        [3] https://github.com/grafoteka/rhex
    """

    def __init__(self,
                 simulator,
                 position=(0, 0, 0.12),
                 orientation=(0, 0, 0, 1),
                 fixed_base=False,
                 scaling=1.,
                 urdf=os.path.dirname(__file__) + '/urdfs/rhex/rhex.urdf'):
        # check parameters
        if position is None:
            position = (0., 0., 0.12)
        if len(position) == 2:  # assume x, y are given
            position = tuple(position) + (0.12,)
        if orientation is None:
            orientation = (0, 0, 0, 1)
        if fixed_base is None:
            fixed_base = False

        super(Rhex, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)
        self.name = 'rhex'

        self.legs = [[self.get_link_ids(link + str(idx))] for link, idx in zip(['leg'] * 6, range(1, 7))
                     if link + str(idx) in self.link_names]

        self.feet = [self.get_link_ids(link + str(idx)) for link, idx in zip(['leg'] * 6, range(1, 7))
                     if link + str(idx) in self.link_names]

        self.leg_axis = np.ones(len(self.feet))

    def drive(self, speed):
        if isinstance(speed, (int, float)):
            speed = speed * np.ones(len(self.feet))
            speed = speed * self.leg_axis
        self.set_joint_velocities(speed, self.feet)


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
    robot = Rhex(sim)

    # print information about the robot
    robot.print_info()

    # Position control using sliders
    # robot.add_joint_slider(robot.right_back_leg)

    # run simulation
    for i in count():
        # robot.update_joint_slider()
        robot.drive(2)
        # step in simulation
        world.step(sleep_dt=1./240)