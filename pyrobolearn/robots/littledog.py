#!/usr/bin/env python
"""Provide the Little Dog robotic platform.
"""

import os
import numpy as np

from pyrobolearn.robots.legged_robot import QuadrupedRobot


class LittleDog(QuadrupedRobot):
    r"""Little Dog

    """

    def __init__(self,
                 simulator,
                 position=(0, 0, 0.2),
                 orientation=(0, 0, 0, 1),
                 fixed_base=False,
                 scaling=1.,
                 urdf=os.path.dirname(__file__) + '/urdfs/littledog/littleDog.urdf'):
        # check parameters
        if position is None:
            position = (0., 0., 0.2)
        if len(position) == 2:  # assume x, y are given
            position = tuple(position) + (0.2,)
        if orientation is None:
            orientation = (0, 0, 0, 1)
        if fixed_base is None:
            fixed_base = False

        super(LittleDog, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)
        self.name = 'littledog'

        self.legs = [[self.get_link_ids(link) for link in links if link in self.link_names]
                     for links in [['front_left_hip', 'front_left_upper_leg', 'front_left_lower_leg'],
                                   ['front_right_hip', 'front_right_upper_leg', 'front_right_lower_leg'],
                                   ['back_left_hip', 'back_left_upper_leg', 'back_left_lower_leg'],
                                   ['back_right_hip', 'back_right_upper_leg', 'back_right_lower_leg']]]

        self.feet = [self.get_link_ids(link) for link in ['front_left_lower_leg', 'front_right_lower_leg',
                                                        'back_left_lower_leg', 'back_right_lower_leg']
                     if link in self.link_names]

        self.kp = 24. * np.ones(12)
        self.kd = np.array([0.5, 0.5, 0.16, 0.5, 0.5, 0.16, 0.5, 0.5, 0.16, 0.5, 0.5, 0.16])

        self.set_joint_positions([-0.6, -0.6, 0.6, 0.6], self.feet)

        self.joint_nominal_config = np.array([0., 0., -0.6, 0., 0., -0.6, 0., 0., 0.6, 0., 0., 0.6])


# Tests
if __name__ == "__main__":
    from itertools import count
    from pyrobolearn.simulators import BulletSim
    from pyrobolearn.worlds import BasicWorld

    # Create simulator
    sim = BulletSim()

    # create world
    world = BasicWorld(sim)

    # create robot
    robot = LittleDog(sim)

    # print information about the robot
    robot.print_info()

    # Position control using sliders
    # robot.add_joint_slider()

    # run simulator
    for _ in count():
        # robot.update_joint_slider()
        # robot.compute_and_draw_com_position()
        # robot.compute_and_draw_projected_com_position()
        world.step(sleep_dt=1./240)