#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016-2018, Eric Jacob <erjac77@gmail.com>
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

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: f5bigip_auth_user
short_description: BIG-IP auth user module
description:
    - Configures user accounts for the BIG-IP system.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    description:
        description:
            - Describes the user account in free form text.
    name:
        description:
            - Specifies unique name for the component.
        required: true
    partition:
        description:
            - Displays the name of the administrative partition in which the user account resides.
        default: Common
    partition_access:
        description:
            - Specifies the administrative partitions to which the user currently has access.
    password:
        description:
            - Sets the user password during creation or modification of a user account without prompting or
              confirmation.
    prompt_for_password:
        description:
            - Indicates that when the account is created or modified, the BIG-IP system prompts the administrator or
              user manager for both a password and a password confirmation for the account.
    shell:
        description:
            - Specifies the shell to which the user has access.
        choices: ['bash', 'none', 'tmsh']
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
requirements:
    - BIG-IP >= 12.0
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create Auth User
  f5bigip_auth_user:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: user1
    partition: Test
    description: User 1
    partition_access:
      - { name: Test, role: operator }
      - { name: Common, role: guest }
    state: present
  delegate_to: localhost
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.base import F5_NAMED_OBJ_ARGS
from ansible_common_f5.base import F5_PROVIDER_ARGS
from ansible_common_f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            description=dict(type='str'),
            partition_access=dict(type='list'),
            password=dict(type='str', no_log=True),
            prompt_for_password=dict(type='str', no_log=True),
            shell=dict(type='str', choices=['bash', 'none', 'tmsh'])
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        del argument_spec['partition']
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpAuthUser(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.auth.users.user.create,
            'read': self._api.tm.auth.users.user.load,
            'update': self._api.tm.auth.users.user.update,
            'delete': self._api.tm.auth.users.user.delete,
            'exists': self._api.tm.auth.users.user.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpAuthUser(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
