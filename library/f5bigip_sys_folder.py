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
module: f5bigip_sys_folder
short_description: BIG-IP sys folder module
description:
    - Configure folders (directory structure) on the BIG-IP system.
version_added: "1.0"
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    description:
        description:
            - Specifies descriptive text that identifies the component.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 1.0
    device_group:
        description:
            - Adds this folder and all configuration items in this folder to a device group for device failover or config-sync purposes.
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
    no_ref_check:
        description:
            - Specifies whether strict device group reference validation is performed on configuration items in the folder.
        required: false
        default: false
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
    traffic_group:
        description:
            - Adds this folder and its configuration items to an existing traffic group.
        required: false
        default: false
        choices: []
        aliases: []
        version_added: 1.0
'''

EXAMPLES = '''
- name: Create SYS Folder
  f5bigip_sys_folder:
    f5bigip_hostname: "172.16.227.35"
    f5bigip_username: "admin"
    f5bigip_password: "admin"
    f5bigip_port: "443"
    name: "my_folder"
    partition: "Common"
    description: "my folder"
    sub_path: "/"
    state: "present"
  delegate_to: localhost
'''

from ansible_common_f5bigip.f5bigip import *

BIGIP_SYS_FOLDER_ARGS = dict(
    #app_service     =   dict(type='str'),
    description     =   dict(type='str'),
    device_group    =   dict(type='str'),
    no_ref_check    =   dict(type='bool'),
    sub_path        =   dict(type='str'),
    traffic_group   =   dict(type='str')
)

class F5BigIpSysFolder(F5BigIpObject):
    def _set_crud_methods(self):
        self.methods = {
            'create':self.mgmt.tm.sys.folders.folder.create,
            'read':self.mgmt.tm.sys.folders.folder.load,
            'update':self.mgmt.tm.sys.folders.folder.update,
            'delete':self.mgmt.tm.sys.folders.folder.delete,
            'exists':self.mgmt.tm.sys.folders.folder.exists
        }
    
    #def read(self):
    #    folder = self.methods['read'](
    #        name=self.params['name'],
    #        partition=self.params['partition']
    #    )
    #    if folder.subPath == folder.name:
    #        folder.subPath = '/'
    #    return folder

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpObject(argument_spec=BIGIP_SYS_FOLDER_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpSysFolder(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except AnsibleModuleF5BigIpError as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':  
    main()