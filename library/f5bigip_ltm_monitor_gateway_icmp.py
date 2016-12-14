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
module: f5bigip_ltm_gateway_icmp
short_description: BIG-IP LTM Gateway ICMP monitor module
description:
    - Configures an Internet Control Message Protocol (ICMP) monitor.
version_added: "1.0"
author:
    - "Eric Jacob, @erjac77"
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
        choices: ['enabled', 'disabled']
        aliases: []
        version_added: 1.0
    adaptive_divergence_type:
        description:
            - Specifies whether the adaptive-divergence-value is relative or absolute.
        required: false
        default: null
        choices: ['relative', 'absolute']
        aliases: []
        version_added: 1.0
    adaptive_divergence_value:
        description:
            - Specifies how far from mean latency each monitor probe is allowed to be.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    adaptive_limit:
        description:
            - Specifies the hard limit, in milliseconds, which the probe is not allowed to exceed, regardless of the divergence value.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    adaptive_sampling_timespan:
        description:
            - Specifies the size of the sliding window, in seconds, which records probe history.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        required: false
        default: http
        choices: []
        aliases: []
        version_added: 1.0
    description:
        description:
            - Specifies descriptive text that identifies the component.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
        required: false
        default: *:*
        choices: []
        aliases: []
        version_added: 1.0
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource is down or the status of the resource is unknown.
        required: false
        default: 5
        choices: []
        aliases: []
        version_added: 1.0
    manual_resume:
        description:
            - Specifies whether the system automatically changes the status of a resource to up at the next successful monitor check.
        required: false
        default: disabled
        choices: ['enabled', 'disabled']
        aliases: []
        version_added: 1.0
    name:
        description:
            - Specifies a unique name for the component.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        required: false
        default: Common
        choices: []
        aliases: []
        version_added: 1.0
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
        version_added: 1.0
    time_until_up:
        description:
            - Specifies the amount of time, in seconds, after the first successful response before a node is marked up.
        required: false
        default: 0
        choices: []
        aliases: []
        version_added: 1.0
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        required: false
        default: 16
        choices: []
        aliases: []
        version_added: 1.0
    transparent:
        description:
            - Specifies whether the monitor operates in transparent mode.
        required: false
        default: disabled
        choices: ['enabled', 'disabled']
        aliases: []
        version_added: 1.0
    up_interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when the resource is up.
        required: false
        default: 0
        choices: []
        aliases: []
        version_added: 1.0
'''

EXAMPLES = '''
- name: Create LTM Gateway ICMP Monitor
  f5bigip_ltm_gateway_icmp:
    f5bigip_hostname: "172.16.227.35"
    f5bigip_username: "admin"
    f5bigip_password: "admin"
    f5bigip_port: "443"
    name: "my_gateway_icmp_monitor"
    partition: "Common"
    state: "present"
  delegate_to: localhost
'''

from ansible_common_f5bigip.f5bigip import *

BIGIP_LTM_MONITOR_GATEWAY_ICMP_ARGS = dict(
    adaptive                    =   dict(type='str', choices=F5BIGIP_ACTIVATION_CHOICES),
    adaptive_divergence_type    =   dict(type='str', choices=['relative', 'absolute']),
    adaptive_divergence_value   =   dict(type='int'),
    adaptive_limit              =   dict(type='int'),
    adaptive_sampling_timespan  =   dict(type='int'),
    #app_service                 =   dict(type='str'),
    defaults_from               =   dict(type='str'),
    description                 =   dict(type='str'),
    destination                 =   dict(type='str'),
    interval                    =   dict(type='int'),
    manual_resume               =   dict(type='str', choices=F5BIGIP_ACTIVATION_CHOICES),
    time_until_up               =   dict(type='int'),
    timeout                     =   dict(type='int'),
    transparent                 =   dict(type='str', choices=F5BIGIP_ACTIVATION_CHOICES),
    up_interval                 =   dict(type='int')
)

class F5BigIpLtmGatewayIcmp(F5BigIpObject):
    def _set_crud_methods(self):
        self.methods = {
            'create':self.mgmt.tm.ltm.monitor.gateway_icmps.gateway_icmp.create,
            'read':self.mgmt.tm.ltm.monitor.gateway_icmps.gateway_icmp.load,
            'update':self.mgmt.tm.ltm.monitor.gateway_icmps.gateway_icmp.update,
            'delete':self.mgmt.tm.ltm.monitor.gateway_icmps.gateway_icmp.delete,
            'exists':self.mgmt.tm.ltm.monitor.gateway_icmps.gateway_icmp.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpObject(argument_spec=BIGIP_LTM_MONITOR_GATEWAY_ICMP_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpLtmGatewayIcmp(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':  
    main()