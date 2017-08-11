#!/usr/bin/python
#
# Copyright 2016, Eric Jacob <erjac77@gmail.com>
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

DOCUMENTATION = '''
---
module: f5bigip_ltm_monitor_tcp_echo
short_description: BIG-IP ltm monitor tcp echo module
description:
    - Configures a Transmission Control Protocol (TCP) Echo monitor.
version_added: 2.3
author:
    - "Gabriel Fortin"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    adaptive:
        description:
            - Specifies whether the adaptive feature is enabled for this monitor.
        required: false
        default: null
        choices: []
        aliases: []
    adaptive_divergence_type:
        description:
            - Specifies whether the adaptive-divergence-value is relative or absolute.
        required: false
        default: null
        choices: ['absolute', 'relative']
        aliases: []
    adaptive_divergence_value:
        description:
            - Specifies how far from mean latency each monitor probe is allowed to be.
        required: false
        default: null
        choices: []
        aliases: []
    adaptive_limit:
        description:
            - Specifies the hard limit, in milliseconds, which the probe is not allowed to exceed, regardless of the divergence value.
        required: false
        default: null
        choices: []
        aliases: []
    adaptive_sampling_timespan:
        description:
            - Specifies the size of the sliding window, in seconds, which records probe history.
        required: false
        default: null
        choices: []
        aliases: []
    app_service:
        description:
            - Specifies the name of the application service to which the monitor belongs.
        required: false
        default: none
        choices: []
        aliases: []
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        required: false
        default: tcp_echo
        choices: []
        aliases: []
    description:
        description:
            - Specifies descriptive text that identifies the component.
        required: false
        default: null
        choices: []
        aliases: []
    destination:
        description:
            - Specifies the IP address of the resource that is the destination of this monitor.
        required: false
        default: null
        choices: []
        aliases: []
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource is down or the status of the resource is unknown.
        required: false
        default: 5
        choices: []
        aliases: []
    manual_resume:
        description:
            - Specifies whether the system automatically changes the status of a resource to up at the next successful monitor check.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    name:
        description:
            - Specifies a unique name for the component.
        required: true
        default: null
        choices: []
        aliases: []
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        required: false
        default: Common
        choices: []
        aliases: []
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
    time_until_up:
        description:
            - Specifies the amount of time, in seconds, after the first successful response before a node is marked up.
        required: false
        default: 0
        choices: []
        aliases: []
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        required: false
        default: 16
        choices: []
        aliases: []
    transparent:
        description:
            - Specifies whether the monitor operates in transparent mode.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    up_interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when the resource is up.
        required: false
        default: 0
        choices: []
        aliases: []
'''

EXAMPLES = '''
- name: Create LTM Monitor TCP Echo
  f5bigip_ltm_monitor_tcp_echo:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_tcp_echo_monitor
    partition: Common
    description: My tcp echo monitor
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_LTM_MONITOR_TCP_ECHO_ARGS = dict(
    adaptive                      =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    adaptive_divergence_type      =    dict(type='str', choices=['absolute', 'relative']),
    adaptive_divergence_value     =    dict(type='int'),
    adaptive_limit                =    dict(type='int'),
    adaptive_sampling_timespan    =    dict(type='int'),
    app_service                   =    dict(type='str'),
    defaults_from                 =    dict(type='str'),
    description                   =    dict(type='str'),
    destination                   =    dict(type='str'),
    interval                      =    dict(type='int'),
    manual_resume                 =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    time_until_up                 =    dict(type='int'),
    timeout                       =    dict(type='int'),
    transparent                   =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    up_interval                   =    dict(type='int')
)

class F5BigIpLtmMonitorTcpEcho(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.ltm.monitor.tcp_echos.tcp_echo.create,
            'read':     self.mgmt_root.tm.ltm.monitor.tcp_echos.tcp_echo.load,
            'update':   self.mgmt_root.tm.ltm.monitor.tcp_echos.tcp_echo.update,
            'delete':   self.mgmt_root.tm.ltm.monitor.tcp_echos.tcp_echo.delete,
            'exists':   self.mgmt_root.tm.ltm.monitor.tcp_echos.tcp_echo.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}

    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_LTM_MONITOR_TCP_ECHO_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpLtmMonitorTcpEcho(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()