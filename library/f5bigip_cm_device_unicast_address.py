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
module: f5bigip_cm_device_unicast_address
short_description: BIG-IP cm device unicast address module
description:
    - Configures unicast addresses for the device.
version_added: "2.4"
author:
    - "Eric Jacob (@erjac77)"
options:
    device:
        description:
            - Specifies the device in which the unicast address belongs.
        required: true
    ip:
        description:
            - Specifies the unicast IP addresses used for failover.
    port:
        description:
            - Specifies the port used for failover.
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
- name: Add CM Device Failover unicast address
  f5bigip_cm_device_unicast_address:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    device: bigip01.localhost
    ip: 10.10.30.11
    port: 1026
    state: present
  delegate_to: localhost
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.f5_bigip import *

BIGIP_CM_DEVICE_UNICAST_ADDRESS_ARGS = dict(
    device  =   dict(type='str'),
    ip      =   dict(type='str'),
    port    =   dict(type='int')
)

class F5BigIpCmDeviceUnicastAddress(F5BigIpUnnamedObject):
    def set_crud_methods(self):
        self.device = self.mgmt_root.tm.cm.devices.device.load(name=self.params['device'])
        del self.params['device']

    def _read(self):
        return self.device

    def flush(self):
        has_changed = False
        found = False
        result = dict()

        for key, val in self.params.iteritems():
            if val is None:
                self.params[key] = 'none'

        device = self._read()
        if hasattr(device, 'unicastAddress'):
            for addr in device.unicastAddress:
                if addr['ip'] == self.params['ip']:
                    found = True
                    if self.state == "absent":
                        has_changed = True
                        device.unicastAddress.remove(addr)
                    if self.state == "present":
                        for key, val in self.params.iteritems():
                            if addr[key] != val:
                                has_changed = True
                                addr[key] = val
            if not found:
                if self.state == "present":
                    has_changed = True
                    device.unicastAddress.append(self.params)
        else:
            if self.state == "present":
                has_changed = True
                device.unicastAddress = [self.params]

        if has_changed:
            device.update()
            device.refresh()

        result.update(dict(changed=has_changed))
        return result

def main():
    module = AnsibleModuleF5BigIpUnnamedObject(argument_spec=BIGIP_CM_DEVICE_UNICAST_ADDRESS_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpCmDeviceUnicastAddress(check_mode=module.supports_check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

if __name__ == '__main__':
    main()