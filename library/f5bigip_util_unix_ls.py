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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: f5bigip_util_unix_ls
short_description: BIG-IP util unix ls module
description:
    - Shows contents of folders.
version_added: 2.3
author:
    - "Gabriel Fortin"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    path:
        description:
            - Specifies the path of the folder.
        required: false
        default: null
        choices: []
        aliases: []
'''

EXAMPLES = '''
- name: Util Unix ls
  f5bigip_util_unix_ls:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    path: /var/
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_UTIL_UNIX_LS_ARGS = dict(
    path    =    dict(type='str', required=True),
)

class F5BigIpUtilUnixLs(F5BigIpUnnamedObject):
    def set_crud_methods(self):
        self.methods = {
            'list':   self.mgmt_root.tm.util.unix_ls.exec_cmd
        }

    def list(self):
        has_changed = False
        
        try:
            obj = self.methods['list']('run', utilCmdArgs=self.params['path'])
            has_changed = True
        except Exception:
            raise AnsibleF5Error('Cant show the contents of this folder.')

        return { 'result': obj.commandResult, 'changed': has_changed }

def main():
    # Translation list for conflictual params
    tr = {}

    module = AnsibleModuleF5BigIpUnnamedObject(argument_spec=BIGIP_UTIL_UNIX_LS_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpUtilUnixLs(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.list()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()