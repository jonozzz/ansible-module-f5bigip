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
module: f5bigip_cm_sync_status
short_description: BIG-IP cm sync status module
description:
    - Displays the configuration synchronization status of the local device.
version_added: 2.3
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
'''

EXAMPLES = '''
- name: Get CM sync status of the device
  f5bigip_cm_sync_status:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_CM_SYNC_STATUS_ARGS = dict(
)

class F5BigIpCmSyncStatus(F5BigIpUnnamedObject):
    def set_crud_methods(self):
        self.methods = {
            'read':     self.mgmt_root.tm.cm.sync_status
        }
    
    def _read(self):
        return self.methods['read']

    def flush(self):
        result = dict()
        has_changed = False
        
        sync_status = self._read()
        if sync_status._meta_data['uri'].endswith("/mgmt/tm/cm/sync-status/"):
        	sync_status.refresh()
        	desc = sync_status.entries['https://localhost/mgmt/tm/cm/sync-status/0']['nestedStats']['entries']['status']['description']
        else:
        	raise AnsibleF5Error("Unable to retrieve the sync status of the device.")
        
        result.update(dict(changed=has_changed, sync_status=desc))
        return result

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpUnnamedObject(argument_spec=BIGIP_CM_SYNC_STATUS_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpCmSyncStatus(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()