#!/usr/bin/env python
"""Provide the HyQ2Max robotic platform.
"""

import os
import numpy as np

from pyrobolearn.robots.legged_robot import QuadrupedRobot


class HyQ2Max(QuadrupedRobot):
    r"""HyQ2Max

    HyQ2Max robot created by IIT.

    References:
        [1] "Design of the Hydraulically-Actuated,Torque-Controlled Quadruped Robot HyQ2Max", Semini et al., 2016
    """

    def __init__(self,
                 simulator,
                 position=(0, 0, 0.8),
                 orientation=(0, 0, 0, 1),
                 fixed_base=False,
                 scaling=1.,
                 urdf=os.path.dirname(__file__) + '/urdfs/hyq2max/hyq2max.urdf'):
        # check parameters
        if position is None:
            position = (0., 0., 0.8)
        if len(position) == 2:  # assume x, y are given
            position = tuple(position) + (0.8,)
        if orientation is None:
            orientation = (0, 0, 0, 1)
        if fixed_base is None:
            fixed_base = False

        super(HyQ2Max, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)
        self.name = 'hyq2max'
        self.height = 0.9

        self.legs = [[self.get_link_ids(link) for link in links if link in self.link_names]
                     for links in [['lf_hipassembly', 'lf_upperleg', 'lf_lowerleg'],
                                   ['rf_hipassembly', 'rf_upperleg', 'rf_lowerleg'],
                                   ['lh_hipassembly', 'lh_upperleg', 'lh_lowerleg'],
                                   ['rh_hipassembly', 'rh_upperleg', 'rh_lowerleg']]]

        self.feet = [self.get_link_ids(link) for link in ['lf_foot', 'rf_foot', 'lh_foot', 'rh_foot']
                     if link in self.link_names]

        for foot in self.feet:
            self.sim.change_dynamics(self.id, foot, lateral_friction=.9, spinning_friction=1., rolling_friction=1.)
            self.sim.change_dynamics(self.id, foot, restitution=0.)

        # taken from "Learning agile and dynamic motor skills for legged robots", Hwangbo et al., 2019
        self.kp = 50. * np.ones(12)
        self.kd = 0.1 * np.ones(12)


# Test
if __name__ == "__main__":
    from itertools import count
    from pyrobolearn.simulators import BulletSim
    from pyrobolearn.worlds import BasicWorld

    # Create simulator
    sim = BulletSim()

    # create world
    world = BasicWorld(sim)
    world.load_japanese_monastery()

    # create robot
    robot = HyQ2Max(sim)

    # print information about the robot
    robot.print_info()

    # Position control using sliders
    # robot.add_joint_slider(robot.getLeftFrontLegIds())

    # run simulator
    for _ in count():
        # robot.update_joint_slider()
        robot.compute_and_draw_com_position()
        robot.compute_and_draw_projected_com_position()

        world.step(sleep_dt=1./240)