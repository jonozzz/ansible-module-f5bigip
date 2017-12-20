#!/usr/bin/python
#
# Copyright 2016-2017, Eric Jacob <erjac77@gmail.com>
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
module: f5bigip_vcmp_guest
short_description: BIG-IP vcmp guest module
description:
    - Configures a VCMP guest
version_added: "2.4"
author:
    - "Ionut Turturica"
options:
    name:
        description:
            - Specifies unique name for the component.
        required: true
    hoastname:
        description:
            - Specifies a FQDN hostname.
    initial_image:
        description:
            - The initial ISO image (must already be imported on the chassis).
        required: true
    management_ip:
        description:
            - IP/prefix for guest management address.
    management_gw:
        description:
            - IP of the gateway.
    cores_per_slot:
        description:
            - Numbers of cores per slot.
    cores_per_slot:
        description:
            - Numbers of cores per slot.
    slots:
        description:
            - Number of slots reserved for this guest.
    vlans:
        description:
            - Vlans assigned to this gues.
    tr_state:
        description:
            - Guest's requested state (e.g. configured, provisioned, deployed). Must use tr field to resolve parameter conflict. See example below.
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create NET Self IP
  f5bigip_vcmp_guest:
    f5_hostname: "{{ inventory_hostname }}"
    f5_username: "{{ bigip_username }}"
    f5_password: "{{ bigip_password }}"
    f5_port: 443
    name: my_guest
    hostname: my-guest.lan
    initial_image: BIGIP-12.1.2.0.0.249.iso
    management_ip: 10.146.55.162/24
    management_gw: 10.146.55.254
    cores_per_slot: 2
    slots: 2
    tr_state: deployed
    tr:
      tr_state: state
    vlans: ['VLAN531']
    state: present
  delegate_to: localhost
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.f5_bigip import *
from ansible_common_f5.f5_base import F5_COMMON_ARGS, F5_COMMON_OBJ_ARGS, F5_COMMON_NAMED_OBJ_ARGS

BIGIP_NET_SELFIP_ARGS = dict(
    name                 =   dict(type='str'),
    hostname             =   dict(type='str'),
    initial_image        =   dict(type='str'),
    management_ip        =   dict(type='str'),
    management_gw        =   dict(type='str'),
    cores_per_slot       =   dict(type='int'),
    tr_state             =   dict(type='str'),
    slots                =   dict(type='int'),
    vlans                =   dict(type='list'),
    tr                   =   dict(type='dict')
)


class AnsibleModuleF5BigIpPartitionlessObject(AnsibleModuleF5BigIpNamedObject):
    """Base class for all F5 BIG-IP named objects"""
    def __init__(self, argument_spec, supports_check_mode, mutually_exclusive=[]):
        merged_arg_spec = dict()
        merged_arg_spec.update(F5_COMMON_ARGS)
        merged_arg_spec.update(F5_COMMON_OBJ_ARGS)
        merged_arg_spec.update(F5_COMMON_NAMED_OBJ_ARGS)
        if argument_spec:
            merged_arg_spec.update(argument_spec)
        merged_arg_spec.pop('partition')
        merged_arg_spec.pop('sub_path')

        super(AnsibleModuleF5NamedObject, self).__init__(argument_spec=merged_arg_spec, supports_check_mode=supports_check_mode, mutually_exclusive=mutually_exclusive)


class F5BigIpVcmpGuest(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.vcmp.guests.guest.create,
            'read':     self.mgmt_root.tm.vcmp.guests.guest.load,
            'update':   self.mgmt_root.tm.vcmp.guests.guest.update,
            'delete':   self.mgmt_root.tm.vcmp.guests.guest.delete,
            'exists':   self.mgmt_root.tm.vcmp.guests.guest.exists
        }

    def _read(self):
        guest = self.methods['read'](
            name=self.params['name']
            #partition=self.params['partition']
        )
        #guest.vlans = [self._strip_partition(x) for x in guest.vlans]
        return guest

def main():
    module = AnsibleModuleF5BigIpPartitionlessObject(argument_spec=BIGIP_NET_SELFIP_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpVcmpGuest(check_mode=module.supports_check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

if __name__ == '__main__':
    main()
