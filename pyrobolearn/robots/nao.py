#!/usr/bin/env python
"""Provide the Nao robotic platform.
"""

import os

from pyrobolearn.robots.legged_robot import BipedRobot
from pyrobolearn.robots.manipulator import BiManipulatorRobot
from pyrobolearn.robots.hand import TwoHand


class Nao(BipedRobot, BiManipulatorRobot, TwoHand):
    r"""Nao robot

    """

    def __init__(self,
                 simulator,
                 position=(0, 0, 0.35),
                 orientation=(0, 0, 0, 1),
                 fixed_base=False,
                 scaling=1.,
                 urdf=os.path.dirname(__file__) + '/urdfs/nao/nao_v40.urdf'):
        # check parameters
        if position is None:
            position = (0., 0., 0.35)
        if len(position) == 2:  # assume x, y are given
            position = tuple(position) + (0.35,)
        if orientation is None:
            orientation = (0, 0, 0, 1)
        if fixed_base is None:
            fixed_base = False

        super(Nao, self).__init__(simulator, urdf, position, orientation, fixed_base, scaling)
        self.name = 'nao'

        self.neck = self.get_link_ids('Neck') if 'Neck' in self.link_names else None
        self.head = self.get_link_ids('Head') if 'Head' in self.link_names else None

        self.legs = [[self.get_link_ids(link) for link in links if link in self.link_names]
                     for links in [['LPelvis', 'LHip', 'LThigh', 'LTibia', 'LAnklePitch', 'l_ankle'],
                                   ['RPelvis', 'RHip', 'RThigh', 'RTibia', 'RAnklePitch', 'r_ankle']]]

        self.feet = [self.get_link_ids(link) for link in ['l_sole', 'r_sole'] if link in self.link_names]

        self.arms = [[self.get_link_ids(link) for link in links if link in self.link_names]
                     for links in [['LShoulder', 'LBicep', 'LElbow', 'LForeArm', 'l_wrist', 'l_gripper'],
                                   ['RShoulder', 'RBicep', 'RElbow', 'RForeArm', 'r_wrist', 'r_gripper']]]

        self.hands = [self.get_link_ids(link) for link in ['l_gripper', 'r_gripper'] if link in self.link_names]

        self.fingers = [[self.get_link_ids(link) for link in links if link in self.link_names]
                        for links in [['LThumb1_link', 'LThumb2_link'],
                                      ['LFinger11_link', 'LFinger12_link', 'LFinger13_link'],
                                      ['LFinger21_link', 'LFinger22_link', 'LFinger23_link'],
                                      ['RThumb1_link', 'RThumb2_link'],
                                      ['RFinger11_link', 'RFinger12_link', 'RFinger13_link'],
                                      ['RFinger21_link', 'RFinger22_link', 'RFinger23_link']]]

        self.left_fingers = [0, 1, 2]
        self.right_fingers = [3, 4, 5]


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
    robot = Nao(sim)

    # print information about the robot
    robot.print_info()

    # Position control using sliders
    # robot.add_joint_slider(robot.getLeftArmIds())

    # run simulator
    for _ in count():
        # robot.update_joint_slider()
        world.step(sleep_dt=1./240)