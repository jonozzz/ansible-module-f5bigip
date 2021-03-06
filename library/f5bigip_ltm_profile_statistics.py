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
module: f5bigip_ltm_profile_statistics
short_description: BIG-IP ltm profile statistics module
description:
    - Configures a Statistics profile.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    app_service:
        description:
            - Specifies the name of the application service to which the profile belongs.
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: stats
    description:
        description:
            - User defined description.
    field1:
        description:
            - Specifies the name of a counter.
    name:
        description:
            - Specifies a unique name for the component.
        required: true
    partition:
        description:
            - Displays the administrative partition within which the component resides.
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
- name: Create LTM Profile statistics
  f5bigip_ltm_profile_statistics:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_statistics_profile
    partition: Common
    description: My statistics profile
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
            app_service=dict(type='str'),
            defaults_from=dict(type='str'),
            description=dict(type='str'),
            field1=dict(type='str'),
            field2=dict(type='str'),
            field3=dict(type='str'),
            field4=dict(type='str'),
            field5=dict(type='str'),
            field6=dict(type='str'),
            field7=dict(type='str'),
            field8=dict(type='str'),
            field9=dict(type='str'),
            field10=dict(type='str'),
            field11=dict(type='str'),
            field12=dict(type='str'),
            field13=dict(type='str'),
            field14=dict(type='str'),
            field15=dict(type='str'),
            field16=dict(type='str'),
            field17=dict(type='str'),
            field18=dict(type='str'),
            field19=dict(type='str'),
            field20=dict(type='str'),
            field21=dict(type='str'),
            field22=dict(type='str'),
            field23=dict(type='str'),
            field24=dict(type='str'),
            field25=dict(type='str'),
            field26=dict(type='str'),
            field27=dict(type='str'),
            field28=dict(type='str'),
            field29=dict(type='str'),
            field30=dict(type='str'),
            field31=dict(type='str'),
            field32=dict(type='str')
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileStatistics(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.ltm.profile.statistics_s.statistics.create,
            'read': self._api.tm.ltm.profile.statistics_s.statistics.load,
            'update': self._api.tm.ltm.profile.statistics_s.statistics.update,
            'delete': self._api.tm.ltm.profile.statistics_s.statistics.delete,
            'exists': self._api.tm.ltm.profile.statistics_s.statistics.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpLtmProfileStatistics(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
