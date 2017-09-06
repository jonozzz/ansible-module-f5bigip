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
module: f5bigip_ltm_profile_iiop
short_description: BIG-IP ltm profile iiop module
description:
    - Configures an Internet Inter-Orb Protocol (IIOP) profile.
version_added: 2.3
author:
    - "Gabriel Fortin"
notes:
    - Requires BIG-IP software version >= 12.0
requirements:
    - f5-sdk
options:
    abort_on_timeout:
        description:
            - Specifies whether the system aborts the connection if there is no response received within the time specified in the timeout option.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    app_service:
        description:
            - Specifies the name of the application service to which the profile belongs.
        required: false
        default: none
        choices: []
        aliases: []
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        required: false
        default: iiop
        choices: []
        aliases: []
    description:
        description:
            - User defined description.
        required: false
        default: null
        choices: []
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
            - Displays the administrative partition within which this profile resides.
        required: false
        default: null
        choices: []
        aliases: []
    persist_object_key:
        description:
            - Specifies whether to persist connections based on the object key in the IIOP request.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    persist_request_id:
        description:
            - Specifies whether to persist connections based on the request ID in the IIOP request.
        required: false
        default: enabled
        choices: ['disabled', 'enabled']
        aliases: []
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
    timeout:
        description:
            - Specifies the request timeout.
        required: false
        default: 30
        choices: []
        aliases: []
'''

EXAMPLES = '''
- name: Create LTM Profile IIOP
  f5bigip_ltm_profile_iiop:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_iiop_profile
    partition: Common
    description: My iiop profile
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_LTM_PROFILE_IIOP_ARGS = dict(
    abort_on_timeout      =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    app_service           =    dict(type='str'),
    defaults_from         =    dict(type='str'),
    description           =    dict(type='str'),
    persist_object_key    =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    persist_request_id    =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    timeout               =    dict(type='int')
)

class F5BigIpLtmProfileIiop(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.ltm.profile.iiops.iiop.create,
            'read':     self.mgmt_root.tm.ltm.profile.iiops.iiop.load,
            'update':   self.mgmt_root.tm.ltm.profile.iiops.iiop.update,
            'delete':   self.mgmt_root.tm.ltm.profile.iiops.iiop.delete,
            'exists':   self.mgmt_root.tm.ltm.profile.iiops.iiop.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}

    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_LTM_PROFILE_IIOP_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpLtmProfileIiop(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()