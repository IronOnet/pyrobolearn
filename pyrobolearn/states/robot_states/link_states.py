#!/usr/bin/env python
"""Define the various link states

This includes notably the link positions and velocities.
"""

from abc import ABCMeta

from pyrobolearn.states.robot_states.robot_states import RobotState


__author__ = "Brian Delhaisse"
__copyright__ = "Copyright 2018, PyRoboLearn"
__credits__ = ["Brian Delhaisse"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brian Delhaisse"
__email__ = "briandelhaisse@gmail.com"
__status__ = "Development"


class LinkState(RobotState):
    r"""Link state of a robot
    """
    __metaclass__ = ABCMeta

    def __init__(self, robot, link_ids=None):
        """
        Initialize the link state.

        Args:
            robot (Robot): robot instance
            link_ids (int, int[N]): link id or list of link ids
        """
        super(LinkState, self).__init__(robot)

        # get links from robot
        if link_ids is None:
            link_ids = range(robot.num_links)
        self.links = link_ids

        # read the data
        self._read()


class LinkPositionState(LinkState):
    r"""Link Position state
    """

    def __init__(self, robot, link_ids=None, wrt_link_id=None):
        self.wrt_link_id = wrt_link_id
        super(LinkPositionState, self).__init__(robot, link_ids)

    def _read(self):
        self.data = self.robot.get_link_positions(self.links, wrt_link_id=self.wrt_link_id)


class LinkWorldPositionState(LinkState):
    r"""Link World Position state
    """

    def __init__(self, robot, link_ids=None):
        super(LinkWorldPositionState, self).__init__(robot, link_ids)

    def _read(self):
        self.data = self.robot.get_link_positions(self.links)


class LinkOrientationState(LinkState):
    r"""Link Orientation state
    """

    def __init__(self, robot, link_ids=None):
        super(LinkOrientationState, self).__init__(robot, link_ids)

    def _read(self):  # TODO: convert
        self.data = self.robot.get_link_orientations(self.links)


class LinkVelocityState(LinkState):
    r"""Link velocity state
    """

    def __init__(self, robot, link_ids=None):
        super(LinkVelocityState, self).__init__(robot, link_ids)

    def _read(self):
        self.data = self.robot.get_link_velocities(self.links)


class LinkLinearVelocityState(LinkState):
    r"""Link linear velocity state
    """

    def __init__(self, robot, link_ids=None):
        super(LinkLinearVelocityState, self).__init__(robot, link_ids)

    def _read(self):
        self.data = self.robot.get_link_linear_velocities(self.links)


class LinkAngularVelocityState(LinkState):
    r"""Link angular velocity state
    """

    def __init__(self, robot, link_ids=None):
        super(LinkAngularVelocityState, self).__init__(robot, link_ids)

    def _read(self):
        self.data = self.robot.get_link_angular_velocities(self.links)