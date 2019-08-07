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
module: f5bigip_ltm_profile_mssql
short_description: BIG-IP ltm profile mssql module
description:
    - Configures a profile to manage mssql(tds) database traffic.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    partition:
        description:
            - Displays the administrative partition within which the profile resides.
    read_pool:
        description:
            - Specifies the pool of MS SQL database servers to which the system sends ready-only requests.
    read_write_split_by_command:
        description:
            - When enabled, the system decides which pool to send the client requests the by the content in the message.
        default: disabled
        choices: ['disabled', 'enabled']
    read_write_split_by_user:
        description:
            - When enabled, the system decides which pool to send the client requests the by user name.
        default: disabled
        choices: ['disabled', 'enabled']
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    user_can_write_by_default:
        description:
            - Specifies whether users have write access by default.
        default: true
        choices: ['false', 'true']
    user_list:
        description:
            - Specifies the users who have read-only access to the MS SQL if user-can-write-by-default is true, or the
              users who have write access to the MS SQL database if user-can-write-by-default is false.
    write_persist_timer:
        description:
            - Specify how many minimum time in milliseconds the connection will be persisted to write-pool after
              connection switch to write pool.
    write_pool:
        description:
            - Specifies the pool of MS SQL database servers to which the system sends requests that are not read-only.
requirements:
    - BIG-IP >= 12.0
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create LTM Profile MSSQL
  f5bigip_ltm_profile_mssql:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_mssql_profile
    partition: Common
    state: present
  delegate_to: localhost
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.base import F5_ACTIVATION_CHOICES
from ansible_common_f5.base import F5_NAMED_OBJ_ARGS
from ansible_common_f5.base import F5_PROVIDER_ARGS
from ansible_common_f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            read_pool=dict(type='str'),
            read_write_split_by_command=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            read_write_split_by_user=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            user_can_write_by_default=dict(type='str', choices=['false', 'true']),
            user_list=dict(type='list'),
            write_persist_timer=dict(type='int'),
            write_pool=dict(type='str')
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileMssql(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.ltm.profile.mssqls.mssql.create,
            'read': self._api.tm.ltm.profile.mssqls.mssql.load,
            'update': self._api.tm.ltm.profile.mssqls.mssql.update,
            'delete': self._api.tm.ltm.profile.mssqls.mssql.delete,
            'exists': self._api.tm.ltm.profile.mssqls.mssql.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpLtmProfileMssql(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
