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
module: f5bigip_net_vlan
short_description: BIG-IP net vlan module
description:
    - Configures a virtual local area network (VLAN).
version_added: "2.4"
author:
    - "Eric Jacob (@erjac77)"
options:
    app_service:
        description:
            - Specifies the application service that the object belongs to.
    auto_lasthop:
        description:
            - Specifies whether auto lasthop is enabled or not.
        default: default
        choices: ['default', 'enabled', 'disabled']
    cmp_hash:
        description:
            - Specifies how the traffic on the VLAN will be disaggregated.
        default: default
        choices: ['default', 'dst-ip', 'src-ip']
    customer_tag:
        description:
            - Specifies a number that the system adds into the header of any double tagged frame passing through the
              VLAN.
    dag_round_robin:
        description:
            - Specifies whether some of the stateless traffic on the VLAN should be disaggregated in a round-robin order
              instead of using static hash.
        choices: ['enabled', 'disabled']
    dag_tunnel:
        description:
            - Specifies whether the ip tunnel traffic on the VLAN should be disaggregated based on the inner ip header
              or outer ip header.
        choices: ['outer', 'inner']
    description:
        description:
            - Specifies descriptive text that identifies the component.
    failsafe:
        description:
            - Enables a fail-safe mechanism that causes the active cluster to fail over to a redundant cluster when loss
              of traffic is detected on a VLAN.
        default: disabled
        choices: ['enabled', 'disabled']
    failsafe_action:
        description:
            - Specifies the action for the system to take when the fail-safe mechanism is triggered.
        default: failover-restart-tm
        choices: ['failover', 'failover-restart-tm', 'reboot', 'restart-all']
    failsafe_timeout:
        description:
            - Specifies the number of seconds that an active unit can run without detecting network traffic on this VLAN
              before it starts a failover.
        default: 90
    interfaces:
        description:
            - Specifies a list of tagged or untagged interfaces and trunks that you want to configure for the VLAN.
    learning:
        description:
            - Specifies whether switch ports placed in the VLAN are configured for switch learning, forwarding only, or
              dropped.
        default: enable-forward
        choices: ['disable-drop', 'disable-forward', 'enable-forward']
    mtu:
        description:
            - Sets a specific maximum transition unit (MTU) for the VLAN.
        default: 1500
    name:
        description:
            - Specifies unique name for the component.
        required: true
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        default: Common
    sflow:
        description:
            - Specifies sFlow settings for the HTTP profile.
        suboptions:
            poll_interval:
                description:
                    - Specifies the maximum interval in seconds between two pollings.
                default: 0
            poll_interval_global:
                description:
                    - Specifies whether the global HTTP poll-interval setting, which is available under sys sflow
                      global-settings module, overrides the object-level poll-interval setting.
                default: yes
                choices: ['no', 'yes']
            sampling_rate:
                description:
                    - Specifies the ratio of packets observed to the samples generated.
                default: 0
            sampling_rate_global:
                description:
                    - Specifies whether the global HTTP sampling-rate setting, which is available under sys sflow
                      global-settings module, overrides the object-level sampling-rate setting.
                default: yes
                choices: ['no', 'yes']
    source_checking:
        description:
            - Specifies that only connections that have a return route in the routing table are accepted.
        default: disabled
        choices: ['enabled', 'disabled']
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    tag:
        description:
            - Specifies a number that the system adds into the header of any frame passing through the VLAN.
requirements:
    - BIG-IP >= 12.0
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create NET VLAN
  f5bigip_net_vlan:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: internal
    partition: Common
    tag: 10
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
            auto_lasthop=dict(type='str', choices=['default', 'enabled', 'disabled']),
            cmp_hash=dict(type='str', choices=['default', 'dst-ip', 'src-ip']),
            customer_tag=dict(type='str'),
            dag_round_robin=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            dag_tunnel=dict(type='str', choices=['outer', 'inner']),
            description=dict(type='str'),
            failsafe=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            failsafe_action=dict(type='str', choices=['failover', 'failover-restart-tm', 'reboot', 'restart-all']),
            failsafe_timeout=dict(type='int'),
            interfaces=dict(type='list'),
            learning=dict(type='str', choices=['disable-drop', 'disable-forward', 'enable-forward']),
            mtu=dict(type='int'),
            sflow=dict(type='dict'),
            source_checking=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            tag=dict(type='int')
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return True


class F5BigIpNetVlan(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.net.vlans.vlan.create,
            'read': self._api.tm.net.vlans.vlan.load,
            'update': self._api.tm.net.vlans.vlan.update,
            'delete': self._api.tm.net.vlans.vlan.delete,
            'exists': self._api.tm.net.vlans.vlan.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpNetVlan(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
