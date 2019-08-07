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
module: f5bigip_ltm_persistence_dest_addr
short_description: BIG-IP ltm persistence dest address module
description:
    - Configures a dest address affinity persistence profile.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    app_service:
        description:
            - Specifies the application service to which the object belongs.
    defaults_from:
        description:
            - Specifies the existing profile from which the system imports settings for the new profile.
        default: dest_addr
    description:
        description:
            - Specifies descriptive text that identifies the component.
    hash_algorithm:
        description:
            - Specifies the system uses hash persistence load balancing.
        default: default
        choices: ['carp', 'default']
    mask:
        description:
            - Specifies an IP mask.
        default: '::'
    match_across_pools:
        description:
            - Specifies, when enabled, that the system can use any pool that contains this persistence record.
        default: disabled
        choices: ['enabled', 'disabled']
    match_across_services:
        description:
            - Specifies, when enabled, that all persistent connections from a client IP address, which go to the same
              virtual IP address, also go to the same node.
        default: disabled
        choices: ['enabled', 'disabled']
    match_across_virtuals:
        description:
            - Specifies, when enabled, that all persistent connections from the same client IP address go to the same
              node.
        default: disabled
        choices: ['enabled', 'disabled']
    mirror:
        description:
            - Specifies whether the system mirrors persistence records to the high-availability peer.
        default: disabled
        choices: ['enabled', 'disabled']
    name:
        description:
            - Specifies a unique name for the component.
        required: true
    override_connection_limit:
        description:
            - Specifies, when enabled, that the pool member connection limits are not enforced for persisted clients.
        default: disabled
        choices: ['enabled', 'disabled']
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        default: Common
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    timeout:
        description:
            - Specifies the duration of the persistence entries.
        default: 180
requirements:
    - BIG-IP >= 12.0
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create LTM Dest Address Persistence profile
  f5bigip_ltm_persistence_dest_addr:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_dest_addr_persistence
    partition: Common
    description: My dest address persistence profile
    defaults_from: dest_addr
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
            defaults_from=dict(type='str'),
            description=dict(type='str'),
            hash_algorithm=dict(type='str', choices=['carp', 'default']),
            mask=dict(type='str'),
            match_across_pools=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            match_across_services=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            match_across_virtuals=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            mirror=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            override_connection_limit=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            timeout=dict(type='int')
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpLtmPersistenceDestAddr(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.ltm.persistence.dest_addrs.dest_addr.create,
            'read': self._api.tm.ltm.persistence.dest_addrs.dest_addr.load,
            'update': self._api.tm.ltm.persistence.dest_addrs.dest_addr.update,
            'delete': self._api.tm.ltm.persistence.dest_addrs.dest_addr.delete,
            'exists': self._api.tm.ltm.persistence.dest_addrs.dest_addr.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpLtmPersistenceDestAddr(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
