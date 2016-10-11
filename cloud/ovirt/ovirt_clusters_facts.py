#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Red Hat, Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

try:
    import ovirtsdk4 as sdk
except ImportError:
    pass

from ansible.module_utils.ovirt import *

DOCUMENTATION = '''
---
module: ovirt_clusters_facts
short_description: Retrieve facts about one or more oVirt clusters
version_added: "2.3"
description:
    - "Retrieve facts about one or more oVirt clusters."
notes:
    - "This module creates a new top-level C(ovirt_clusters) fact, which
       contains a list of clusters."
requirements:
    - python >= 2.7
    - ovirt-engine-sdk-python >= 4.0.0
options:
   name:
     description:
       - Restrict results to clusters with names matching this glob expression (e.g., C<production*>).
     required: false
     default: None
'''

EXAMPLES = '''
# Examples don't contain auth parameter for simplicity,
# look at ovirt_auth module to see how to reuse authentication:

# Gather facts about all clusters named C<production*>:
- ovirt_clusters_facts:
    name: web*
- debug:
    var: ovirt_clusters
'''


def main():
    argument_spec = ovirt_full_argument_spec(
        name=dict(default=None, required=False),
    )
    module = AnsibleModule(argument_spec)
    check_sdk(module)

    try:
        connection = create_connection(module.params.pop('auth'))
        clusters_service = connection.system_service().clusters_service()
        clusters = clusters_service.list(
            search='name=%s' % module.params['name'] if module.params['name'] else None
        )
        module.exit_json(
            changed=False,
            ansible_facts=dict(
                ovirt_clusters=[
                    get_dict_of_struct(c) for c in clusters
                ],
            ),
        )
    except Exception as e:
        module.fail_json(msg=str(e))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
