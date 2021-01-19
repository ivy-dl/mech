"""
Collection of Pose Conversion Functions to Axis-Angle Pose Format
"""

# global
from ivy.framework_handler import get_framework as _get_framework

# local
from ivy_mech.orientation import quaternion as _ivy_quat
from ivy_mech.orientation import axis_angle as _ivy_aa


def euler_pose_to_axis_angle_pose(euler_pose, convention='zyx', batch_shape=None, dev=None, f=None):
    """
    Convert :math: Euler angle pose
    :math:`\mathbf{p}_{abc} = [\mathbf{x}_c, \mathbf{θ}_{xyz}] = [x, y, z, ϕ_a, ϕ_b, ϕ_c]` to
    axis-angle pose :math:`\mathbf{p}_{aa} = [\mathbf{x}_c, \mathbf{e}, θ] = [x, y, z, e_x, e_y, e_z, θ]`

    :param euler_pose: Euler angle pose *[batch_shape,6]*
    :type euler_pose: array
    :param convention: The axes for euler rotation, in order of L.H.S. matrix multiplication.
    :type convention: str, optional
    :param batch_shape: Shape of batch. Inferred from inputs if None.
    :type batch_shape: sequence of ints, optional
    :param dev: device on which to create the array 'cuda:0', 'cuda:1', 'cpu' etc. Same as x if None.
    :type dev: str, optional
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Rotation axis unit vector and angle *[batch_shape,4]*
    """
    f = _get_framework(euler_pose, f=f)
    aa = _ivy_aa.euler_to_axis_angle(euler_pose[..., 3:], convention, batch_shape, dev, f)
    return f.concatenate([euler_pose[..., :3], aa], -1)


# noinspection PyUnresolvedReferences
def mat_pose_to_rot_vec_pose(matrix, f=None):
    """
    Convert matrix pose :math:`\mathbf{P}\in\mathbb{R}^{3×4}` to rotation vector pose
    :math:`\mathbf{p}_{rv} = [\mathbf{x}_c, \mathbf{θ}_{rv}] = [x, y, z, θe_x, θe_y, θe_z]`.\n
    `[reference] <https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Euler_axis_and_angle_(rotation_vector)>`_

    :param matrix: Matrix pose *[batch_shape,3,4]*
    :type matrix: array
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Rotation vector pose *[batch_shape,6]*
    """

    f = _get_framework(matrix, f=f)

    # BS x 3
    translation = matrix[..., -1]

    # BS x 4
    quaternion = _ivy_quat.rot_mat_to_quaternion(matrix[..., 0:3], f=f)

    # BS x 3
    rot_vector = _ivy_aa.quaternion_to_rotation_vector(quaternion, f=f)

    # BS x 6
    return f.concatenate((translation, rot_vector), -1)


# noinspection PyUnresolvedReferences
def quaternion_pose_to_rot_vec_pose(quat_pose, f=None):
    """
    Convert quaternion pose :math:`\mathbf{p}_{q} = [\mathbf{x}_c, \mathbf{q}] = [x, y, z, q_i, q_j, q_k, q_r]` to
    rotation vector pose :math:`\mathbf{p}_{rv} = [\mathbf{x}_c, \mathbf{θ}_{rv}] = [x, y, z, θe_x, θe_y, θe_z]`.\n
    `[reference] <https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Euler_axis_and_angle_(rotation_vector)>`_

    :param quat_pose: Quaternion pose *[batch_shape,7]*
    :type quat_pose: array
    :param f: Machine learning framework. Inferred from inputs if None.
    :type f: ml_framework, optional
    :return: Rotation vector pose *[batch_shape,6]*
    """

    f = _get_framework(quat_pose, f=f)

    # BS x 4
    vector_and_angle = _ivy_aa.quaternion_to_axis_angle(quat_pose[..., 3:])

    # BS x 3
    rot_vec = vector_and_angle[..., :-1] * vector_and_angle[..., -1:]

    # BS x 6
    return f.concatenate((quat_pose[..., 0:3], rot_vec), -1)