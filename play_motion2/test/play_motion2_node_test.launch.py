# Copyright (c) 2022 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_pal.include_utils import include_launch_py_description
import launch_testing


def generate_test_description():

    pm2_dir = get_package_share_directory('play_motion2')

    rrbot = include_launch_py_description(
        'play_motion2', ['test', 'rrbot.launch.py'])

    play_motion2 = include_launch_py_description(
        'play_motion2', ['launch', 'play_motion2.launch.py'],
        launch_arguments={
          'play_motion2_config': os.path.join(pm2_dir, 'test', 'play_motion2_config.yaml')
        }.items()
    )

    play_motion2_node_test = launch_testing.actions.GTest(
        path=os.path.join(pm2_dir, 'test', 'play_motion2_node_test'),
        output='screen')

    ld = LaunchDescription()

    ld.add_action(rrbot)
    ld.add_action(play_motion2)
    ld.add_action(play_motion2_node_test)

    ld.add_action(launch_testing.actions.ReadyToTest())

    context = {'play_motion2_node_test': play_motion2_node_test}

    return ld, context


class TestPlayMotion(unittest.TestCase):

    def test_wait(self, play_motion2_node_test, proc_info):
        proc_info.assertWaitForShutdown(process=play_motion2_node_test, timeout=(60))


@launch_testing.post_shutdown_test()
class TestProcessOutput(unittest.TestCase):

    def test_exit_code(self, play_motion2_node_test, proc_info):
        launch_testing.asserts.assertExitCodes(
            proc_info, process=play_motion2_node_test)
