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
module: f5bigip_ltm_profile_radius
short_description: BIG-IP ltm profile radius module
description:
    - Configures a RADIUS profile for network traffic load balancing.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    app_service:
        description:
            - Specifies the name of the application service to which the profile belongs.
    clients:
        description:
            - Specifies host and network addresses from which clients can connect.
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        default: radiusLB
    description:
        description:
            - User defined description.
    name:
        description:
            - Specifies a unique name for the component.
        required: true
    partition:
        description:
            - Displays the administrative partition within which the component resides.
    persist_avp:
        description:
            - Specifies the name of the RADIUS attribute on which traffic persists.
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    subscriber_aware:
        description:
            - Specifies whether to extract subscriber information from RADIUS packets.
        default: disabled
        choices: ['disabled', 'enabled']
    subscriber_id_type:
        description:
            - Specifies the RADIUS attribute to be used as the subscriber Id when extracting subscriber information from
              the RADIUS message.
        default: 3gpp-imsi
        choices: ['3gpp-imsi', 'calling-station-id', 'user-name']
requirements:
    - BIG-IP >= 12.0
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create LTM Profile RADIUS
  f5bigip_ltm_profile_radius:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_radius_profile
    partition: Common
    description: My radius profile
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
            app_service=dict(type='str'),
            clients=dict(type='str'),
            defaults_from=dict(type='str'),
            description=dict(type='str'),
            persist_avp=dict(type='str'),
            subscriber_aware=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            subscriber_id_type=dict(type='str', choices=['3gpp-imsi', 'calling-station-id', 'user-name'])
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmProfileRadius(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.ltm.profile.radius_s.radius.create,
            'read': self._api.tm.ltm.profile.radius_s.radius.load,
            'update': self._api.tm.ltm.profile.radius_s.radius.update,
            'delete': self._api.tm.ltm.profile.radius_s.radius.delete,
            'exists': self._api.tm.ltm.profile.radius_s.radius.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpLtmProfileRadius(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
