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
module: f5bigip_net_route_domain
short_description: BIG-IP net route-domain module
description:
    - Configures route-domains for traffic management.
version_added: "1.0"
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    id:
        description:
            - Specifies a unique numeric identifier for the route-domain.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    name:
        description:
            - Specifies unique name for the component.
        required: true
        default: null
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
'''

EXAMPLES = '''
- name: Create NET Route-Domain
  f5bigip_net_route_domain:
    f5bigip_hostname: "172.16.227.35"
    f5bigip_username: "admin"
    f5bigip_password: "admin"
    f5bigip_port: "443"
    name: "my_route_domain"
    id: 1234
    state: "present"
  delegate_to: localhost
'''

from ansible_common_f5bigip.f5bigip import *

BIGIP_NET_ROUTE_DOMAIN_ARGS = dict(
    #app_service             =   dict(type='str'),
    #bwc_policy              =   dict(type='str'),
    #connection_limit        =   dict(type='int'),
    #description             =   dict(type='str'),
    #flow_eviction_policy    =   dict(type='str'),
    #fw_enforced_policy      =   dict(type='str'),
    #fw_rules                =   dict(type='list'),
    #fw_staged_policy        =   dict(type='str'),
    id                      =   dict(type='int')#,
    #parent                  =   dict(type='str'),
    #strict                  =   dict(type='str', choices=F5BIGIP_ACTIVATION_CHOICES),
    #routing_protocol        =   dict(type='list'),
    #vlans                   =   dict(type='list')
)

class F5BigIpNetRouteDomain(F5BigIpObject):
    def _set_crud_methods(self):
        self.methods = {
            'create':self.mgmt.tm.net.route_domains.route_domain.create,
            'read':self.mgmt.tm.net.route_domains.route_domain.load,
            'update':self.mgmt.tm.net.route_domains.route_domain.update,
            'delete':self.mgmt.tm.net.route_domains.route_domain.delete,
            'exists':self.mgmt.tm.net.route_domains.route_domain.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpObject(argument_spec=BIGIP_NET_ROUTE_DOMAIN_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpNetRouteDomain(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':  
    main()