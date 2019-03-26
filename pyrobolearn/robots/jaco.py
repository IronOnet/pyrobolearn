#!/usr/bin/env python
"""Provide the Jaco robotic platform.
"""

import os

from pyrobolearn.robots.manipulator import ManipulatorRobot


class Jaco(ManipulatorRobot):
    r"""Jaco (manipulator) robot

    References:
        [1] https://github.com/JenniferBuehler/jaco-arm-pkgs
        [2] https://github.com/Kinovarobotics/kinova-ros
        [3] https://github.com/RIVeR-Lab/wpi_jaco
    """

    def __init__(self,
                 simulator,
                 position=(0, 0, 0),
                 orientation=(0, 0, 0, 1),
                 fixed_base=True,
                 scaling=1.,
                 urdf=os.path.dirname(__file__) + '/urdfs/jaco/jaco.urdf'):
        # check parameters
        if position is None:
            position = (0., 0., 0.)
        if len(position) == 2:  # assume x, y are given
            position = tuple(position) + (0.,)
        if orientation is None:
            orientation = (0, 0, 0, 1)
        if fixed_base is None:
            fixed_base = True

        super(Jaco, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)
        self.name = 'jaco'


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
    robot = Jaco(sim)

    # print information about the robot
    robot.print_info()

    # run simulation
    for i in count():
        # step in simulation
        world.step(sleep_dt=1./240)