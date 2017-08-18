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
module: f5bigip_net_tunnel_gre
short_description: BIG-IP net tunnel gre module
description:
    - Configures a Generic Router Encapsulation (GRE) profile.
version_added: 2.3
author:
    - "Gabriel Fortin"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    app_service:
        description:
            - Specifies the name of the application service to which the object belongs.
        required: false
        default: null
        choices: []
        aliases: []
    defaults_from:
        description:
            - Specifies the existing profile from which the system imports settings for the new profile.
        required: false
        default: gre
        choices: []
        aliases: []
    description:
        description:
            - User defined description.
        required: false
        default: null
        choices: []
        aliases: []
    encapsulation:
        description:
            - Specifies the flavor of GRE header to use for encapsulation.
        required: false
        default: standard
        choices: ['standard', 'nvgre']
        aliases: []
    flooding_type:
        description:
            - Specifies the flooding type to use to transmit broadcast and unknown destination frames.
        required: false
        default: none
        choices: ['none', 'multipoint']
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
    rx_csum:
        description:
            - Specifies whether the system verifies the checksum on received packets.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
    tx_csum:
        description:
            - Specifies whether the system includes a checksum on transmitted packets.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
'''

EXAMPLES = '''
- name: Create NET Tunnel GRE
  f5bigip_net_tunnel_gre:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_gre_tunnel
    partition: Common
    description: My gre tunnel
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_NET_TUNNEL_GRE_ARGS = dict(
    app_service      =    dict(type='str'),
    defaults_from    =    dict(type='str'),
    description      =    dict(type='str'),
    encapsulation    =    dict(type='str', choices=['standard', 'nvgre']),
    flooding_type    =    dict(type='str', choices=['none', 'multipoint']),
    rx_csum          =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    tx_csum          =    dict(type='str', choices=F5_ACTIVATION_CHOICES)
)

class F5BigIpNetTunnelGre(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.net.tunnels.gres.gre.create,
            'read':     self.mgmt_root.tm.net.tunnels.gres.gre.load,
            'update':   self.mgmt_root.tm.net.tunnels.gres.gre.update,
            'delete':   self.mgmt_root.tm.net.tunnels.gres.gre.delete,
            'exists':   self.mgmt_root.tm.net.tunnels.gres.gre.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}

    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_NET_TUNNEL_GRE_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpNetTunnelGre(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()