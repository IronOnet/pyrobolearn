#!/usr/bin/env python
r"""Provide the various constraints used in QP.

Provide the various optimization constraints (:math:`G, h, F, c` in the upcoming formulation) used in QP.

A quadratic program (QP) is written in standard form [1] as:

.. math::

    x^* &= \arg \min_x \frac{1}{2} x^T Q x + p^T x \\ \text{subj. to}
        & Gx \leq h \\
        & Fx = c

where :math:`x` is the vector being optimized (in robotics, it can be joint positions, velocities, torques, ...),
"the matrix :math:`Q` and vector :math:`p` are used to define any quadratic objective function of these variables,
while the matrix-vector couples :math:`(G,h)` and :math:`(F,c)` respectively define inequality and equality
constraints" [1]. Inequality constraints can include the lower bounds and upper bounds of :math`x` by setting
:math:`G` to be the identity matrix or minus this one, and :math:`h` to be the upper or lower bounds.

For instance, the quadratic objective function :math:`||Ax - b||^2_{W}` (where :math:`W` is a weight matrix) is given
in the standard form as:

.. math:: ||Ax - b||^2_{W} = (Ax - b)^\top W (Ax - b) = x^\top A^\top W A x - 2 b^\top W A x + b^\top W b

where the last term :math:`b^\top W b` can be removed as it does not depend on the variables we are optimizing (i.e.
:math:`x`). We thus have :math:`Q = A^\top W A` a symmetric matrix and :math:`p = -2 b^\top W A`.

Many control problems in robotics can be formulated as a quadratic programming problem.

For instance, let's assume that we want to optimize the joint velocities :math:`\dot{q}` given the end-effector's
desired position and velocity in task space. We can define the quadratic problem as:

.. math:: || J(q) \dot{q} - \dot{x} ) ||^2

where using a PD reference, :math:`\dot{x} = \dot{x}_d + K (x_d - x)`, where :math:`x_d` and :math:`x` are the desired
and current end-effector's position respectively, and :math:`\dot{x}_d` is the desired velocity.


* Soft priority tasks: with soft-priority tasks, the quadratic programming problem being minimized for n such tasks
is given by:

.. math::

    x^* &= \arg \min_x ||A_1 x - b_1||^2_{W_1} + ||A_2 x - b_2 ||^2_{W_2} + ... + ||A_n x - b_n ||^2_{W_n} \\
    \text{subj. to} & Gx \leq h \\
                    & Fx = c

Often, the weight matrices :math:`W_i` are just scalars :math:`w_i`. This problem can notably be solved by stacking
the :math:`A_i` one of top of another, and stacking the :math:`b_i` and :math:`W_i` in the same manner, and solving
:math:`||A x - b||^2_{W}` This is known as the augmented task. When the matrices :math:`A` are Jacobians this is known
as the augmented Jacobian (which can sometimes be ill-conditioned).

* Hard priority tasks: with hard-priority tasks, the quadratic programming problem for n tasks is defined in a
sequential manner, where the first most important task will be first optimized, and then the subsequent tasks will be
optimized one after the other. Thus, the first task to be optimized is given by:

.. math:: x_1^* &= \arg \min_x ||A_1 x - b_1||^2 \\ \text{subj. to}
                & G_1 x \leq h_1 \\
                & F_1 x = c_1,

while the second next most important task that would be solved is given by:

.. math:: x_2^* &= \arg \min_x ||A_2 x - b_2||^2 \\ \text{subj. to}
                & G_2 x \leq h_2 \\
                & F_2 x = c_2 \\
                & A_1 x = A_1 x_1^* \\
                & G_1 x \leq h_1 \\
                & F_1 x = c_1,

until the :math:`n` most important task, given by:

.. math:: x_n^* \arg \min_x ||A_n x - b_n||^2 \\ \text{subj. to}
                & A_1 x = A_1 x_1^* \\
                & ... \\
                & A_{n-1} x = A_{n-1} x_{n-1}^* \\
                & G_1 x \leq h_1 \\
                & ... \\
                & G_n x \leq h_n \\
                & F_1 x = c_1 \\
                & ... \\
                & F_n x = c_n.

By setting the previous :math:`A_{i-1} x = A_{i-1} x_{i-1}^*` as equality constraints, the current solution
:math:`x_i^*` won't change the optimality of all higher priority tasks.


References:
    [1] "Quadratic Programming in Python" (https://scaron.info/blog/quadratic-programming-in-python.html), Caron, 2017
    [2] "OpenSoT: A whole-body control library for the compliant humanoid robot COMAN", Rocchi et al., 2015
    [3] "Robot Control for Dummies: Insights and Examples using OpenSoT", Hoffman et al., 2017
"""

import numpy as np

__author__ = "Brian Delhaisse"
__copyright__ = "Copyright 2018, PyRoboLearn"
__credits__ = ["OpenSoT (Enrico Mingo Hoffman and Alessio Rocchi)", "Songyan Xin"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brian Delhaisse"
__email__ = "briandelhaisse@gmail.com"
__status__ = "Development"


class Constraint(object):
    r"""Constraint (abstract) class.

    Python implementation of Constraints based on the slides of the OpenSoT framework [1].

    References:
        [1] "OpenSoT: A whole-body control library for the compliant humanoid robot COMAN"
            ([code](https://opensot.wixsite.com/opensot),
            [slides](https://docs.google.com/presentation/d/1kwJsAnVi_3ADtqFSTP8wq3JOGLcvDV_ypcEEjPHnCEA),
            [tutorial video](https://www.youtube.com/watch?v=yFon-ZDdSyg),
            [old code](https://github.com/songcheng/OpenSoT)), Rocchi et al., 2015
    """

    def __init__(self, model):
        """
        Initialize the Constraint.

        Args:
            model (robot, str): robot model.
        """
        self._model = model

    ##############
    # Properties #
    ##############

    @property
    def model(self):
        """Return the robot model."""
        return self._model

    @property
    def lower_bound(self):
        """Return the lower bound."""
        return self._lower_bound

    @property
    def upper_bound(self):
        """Return the upper bound."""
        return self._upper_bound

    @property
    def A_eq(self):
        """Return the :math:`A_{eq}` matrix."""
        return self._A_eq

    @property
    def b_eq(self):
        """Return the :math:`b_{eq}` vector"""
        return self._b_eq

    ###########
    # Methods #
    ###########

    def update(self):
        pass

    #############
    # Operators #
    #############

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__

    def __call__(self):
        return self.update()