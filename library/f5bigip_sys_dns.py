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
module: f5bigip_sys_dns
short_description: BIG-IP sys ntp module
description:
    - Configures the Domain Name System (DNS) for the BIG-IP system.
version_added: "1.0"
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    description:
        description:
            - Specifies descriptive text that identifies the component.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    name_servers:
        description:
            - Configures a group of DNS name servers for the BIG-IP system.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    search:
        description:
            - Configures a list of domain names in a specific order.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
'''

EXAMPLES = '''
- name: Add SYS DNS Name Servers
  f5bigip_sys_dns:
    f5bigip_hostname: "172.16.227.35"
    f5bigip_username: "admin"
    f5bigip_password: "admin"
    f5bigip_port: "443"
    name_servers:
      - 172.16.227.11
      - 172.16.227.12
    state: "present"
  delegate_to: localhost
'''

from ansible_common_f5bigip.f5bigip import *

BIGIP_SYS_DNS_ARGS = dict(
    description     =   dict(type='str'),
    name_servers    =   dict(type='list'),
    search          =   dict(type='list')
)

class F5BigIpSysDns(F5BigIpUnnamedObject):
    def _set_crud_methods(self):
        self.methods = {
            'read':self.mgmt.tm.sys.dns.load,
            'update':self.mgmt.tm.sys.dns.update
        }
    
    def _absent(self):
        if not (self.params['nameServers'] or self.params['search']):
            raise AnsibleModuleF5BigIpError("Absent can only be used when removing name servers or search domains")
        
        return super(F5BigIpSysDns, self)._absent()

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpUnnamedObject(argument_spec=BIGIP_SYS_DNS_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpSysDns(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':  
    main()