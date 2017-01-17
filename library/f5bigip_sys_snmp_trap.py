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
module: f5bigip_sys_snmp_trap
short_description: BIG-IP sys snmp trap module
description:
    - Configures the simple network management protocol (SNMP) traps.
version_added: "1.0"
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    auth_password:
        description:
            - Specifies the authentication password, which must be at least eight characters long.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    auth_protocol:
        description:
            - Specifies the authentication method to use to deliver the trap message.
        required: false
        default: none
        choices: ['md5', 'sha', 'none']
        aliases: []
        version_added: 1.0
    community:
        description:
            - Specifies a community that has access to the trap message.
        required: false
        default: null
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
    engine_id:
        description:
            - Specifies the unique authoritative security engine ID.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    host:
        description:
            - Specifies the trap destination that you are configuring, the IP address, FQDN, or either of these with an embedded protocol.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    port:
        description:
            - Specifies the port for the trap destination that you are configuring.
        required: false
        default: 162
        choices: []
        aliases: []
        version_added: 1.0
    privacy_password:
        description:
            - Specifies the privacy password, which must be at least eight characters long.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    privacy_protocol:
        description:
            - Specifies the encryption/privacy method to use to deliver the trap message.
        required: false
        default: none
        choices: ['aes', 'des', 'none']
        aliases: []
        version_added: 1.0
    security_level:
        description:
            - Specifies the security level to use to deliver the trap message.
        required: false
        default: no-auth-no-privacy
        choices: ['auth-no-privacy', 'auth-privacy', 'no-auth-no-privacy']
        aliases: []
        version_added: 1.0
    security_name:
        description:
            - Specifies the security name the system uses to handle SNMP version 3 trap message.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    version:
        description:
            - Specifies the security model to use.
        required: false
        default: 2c
        choices: ['1', '2c', '3']
        aliases: []
        version_added: 1.0
'''

EXAMPLES = '''
- name: Add SYS SNMP trap
  f5bigip_sys_snmp_trap:
    f5bigip_hostname: "172.16.227.35"
    f5bigip_username: "admin"
    f5bigip_password: "admin"
    f5bigip_port: "443"
    name: "i172_16_227_140_1"
    community: "mycommunity1"
    host: "172.16.227.140"
    port: 162
    version: "2c"
    state: "present"
  delegate_to: localhost
'''

from ansible_common_f5bigip.f5bigip import *

BIGIP_SYS_SNMP_TRAP_ARGS = dict(
    auth_password       =   dict(type='str'),
    auth_protocol       =   dict(type='str', choices=['md5', 'sha', 'none']),
    community           =   dict(type='str'),
    description         =   dict(type='str'),
    engine_id           =   dict(type='str'),
    host                =   dict(type='str'),
    port                =   dict(type='int'),
    privacy_password    =   dict(type='str'),
    privacy_protocol    =   dict(type='str', choices=['aes', 'des', 'none']),
    security_level      =   dict(type='str', choices=['auth-no-privacy', 'auth-privacy', 'no-auth-no-privacy']),
    security_name       =   dict(type='str'),
    version             =   dict(type='str', choices=['1', '2c', '3'])
)

class F5BigIpSysSnmpTrap(F5BigIpObject):
    def _set_crud_methods(self):
        self.snmp = self.mgmt.tm.sys.snmp.load()
        self.methods = {
            'create':self.snmp.traps_s.trap.create,
            'read':self.snmp.traps_s.trap.load,
            'update':self.snmp.traps_s.trap.update,
            'delete':self.snmp.traps_s.trap.delete,
            'exists':self.snmp.traps_s.trap.exists
        }
    
    # exists() returns always True...
    def _exists(self):
        exists = False
        
        try:
            trap = self._read()
            
            if hasattr(trap, 'host'):
                exists = True
        except Exception as exc:
            pass
        
        return exists

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpObject(argument_spec=BIGIP_SYS_SNMP_TRAP_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpSysSnmpTrap(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':  
    main()