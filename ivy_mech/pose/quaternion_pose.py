"""
Collection of Pose Conversion Functions to Quaternion Pose Format
"""

# global
from ivy.framework_handler import get_framework as _get_framework

# local
from ivy_mech.orientation import quaternion as _ivy_quat
from ivy_mech.pose import matrix_pose as _ivy_mat_pose


def axis_angle_pose_to_quaternion_pose(axis_angle_pose, f=None):
    """
    Convert axis-angle pose :math:`\mathbf{p}_{aa} = [\mathbf{x}_c, \mathbf{e}, θ] = [x, y, z, e_x, e_y, e_z, θ]`
    to quaternion pose :math:`\mathbf{p}_{q} = [\mathbf{x}_c, \mathbf{q}] = [x, y, z, q_i, q_j, q_k, q_r]`.

    :param axis_angle_pose: Axis-angle pose *[batch_shape,7]*
    :type axis_angle_pose: array
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Quaternion pose *[batch_shape,7]*
    """

    f = _get_framework(axis_angle_pose, f=f)

    # BS x 3
    translation = axis_angle_pose[..., :3]

    # BS x 7
    return f.concatenate((translation, _ivy_quat.axis_angle_to_quaternion(
        axis_angle_pose[..., 3:], f=f)), -1)


def mat_pose_to_quaternion_pose(matrix, f=None):
    """
    Convert matrix pose :math:`\mathbf{P}\in\mathbb{R}^{3×4}` to quaternion pose
    :math:`\mathbf{p}_{q} = [\mathbf{x}_c, \mathbf{q}] = [x, y, z, q_i, q_j, q_k, q_r]`.\n
    `[reference] <http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/>`_

    :param matrix: Matrix pose *[batch_shape,3,4]*
    :type matrix: array
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Quaternion pose *[batch_shape,7]*
    """

    f = _get_framework(matrix, f=f)

    # BS x 7
    return f.concatenate((matrix[..., 0:3, -1],
                             _ivy_quat.rot_mat_to_quaternion(matrix[..., 0:3, 0:3], f=f)), -1)


def euler_pose_to_quaternion_pose(euler_pose, convention='zyx', batch_shape=None, f=None):
    """
    Convert :math: Euler angle pose
    :math:`\mathbf{p}_{abc} = [\mathbf{x}_c, \mathbf{θ}_{xyz}] = [x, y, z, ϕ_a, ϕ_b, ϕ_c]` to quaternion pose
    :math:`\mathbf{p}_{q} = [\mathbf{x}_c, \mathbf{q}] = [x, y, z, q_i, q_j, q_k, q_r]`.\n
    `[reference] <http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/>`_

    :param euler_pose: Euler angle pose *[batch_shape,6]*
    :type euler_pose: array
    :param convention: The axes for euler rotation, in order of L.H.S. matrix multiplication.
    :type convention: str, optional
    :param batch_shape: Shape of batch. Inferred from inputs if None.
    :type batch_shape: sequence of ints, optional
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Quaternion pose *[batch_shape,7]*
    """

    f = _get_framework(euler_pose, f=f)

    if batch_shape is None:
        batch_shape = euler_pose.shape[:-1]

    # BS x 7
    return mat_pose_to_quaternion_pose(_ivy_mat_pose.euler_pose_to_mat_pose(euler_pose, convention, batch_shape, f=f))


def increment_quaternion_pose_with_velocity(quat_pose, quat_vel, delta_t, f=None):
    """
    Increment a quaternion pose :math:`\mathbf{p}_{q} = [\mathbf{x}_c, \mathbf{q}] = [x, y, z, q_i, q_j, q_k, q_r]`
    forward by one time-increment :math:`Δt`, given the velocity represented in quaternion form :math:`\mathbf{V}_q`.
    Where :math:`\mathbf{P}_q (t+1) = \mathbf{P}_q(t) × \mathbf{V}_q`, :math:`t` is in seconds, and :math:`×` denotes
    the hamilton product.\n
    `[reference] <https://en.wikipedia.org/wiki/Quaternion>`_

    :param quat_pose: Quaternion pose. *[batch_shape,7]*
    :type quat_pose: array
    :param quat_vel: Quaternion velocity. *[batch_shape,7]*
    :type quat_vel: array
    :param delta_t: Time step in seconds, for incrementing the quaternion pose by the velocity quaternion.
    :type delta_t: float
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Incremented quaternion pose *[batch_shape,7]*
    """

    f = _get_framework(quat_pose, f=f)

    # BS x 4
    current_quaternion = quat_pose[..., 3:7]
    quaternion_vel = quat_vel[..., 3:7]
    quaternion_transform = _ivy_quat.scale_quaternion_rotation_angle(quaternion_vel, delta_t, f=f)
    new_quaternion = _ivy_quat.hamilton_product(current_quaternion, quaternion_transform, f=f)

    # BS x 7
    return f.concatenate((quat_pose[..., 0:3] + quat_vel[..., 0:3] * delta_t, new_quaternion), -1)