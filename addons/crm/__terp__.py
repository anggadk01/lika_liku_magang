# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2008 Tiny SPRL (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################
{
    "name" : "Customer & Supplier Relationship Management",
    "version" : "1.0",
    "author" : "Tiny",
    "website" : "http://tinyerp.com/module_crm.html",
    "category" : "Generic Modules/CRM & SRM",
    "description": """The Tiny ERP case and request tracker enables a group of
people to intelligently and efficiently manage tasks, issues, and requests.
It manages key tasks such as communication, identification, prioritization,
assignment, resolution and notification.

Tiny ERP ensures that all cases are successfly tracked by users, customers and
suppliers. It can automatically send reminders, escalate the request, trigger
specific methods and lots of others actions based on your enterprise own rules.

The greatest thing about this system is that users don't need to do anything
special. They can just send email to the request tracker. Tiny ERP will take
care of thanking them for their message, automatically routing it to the
appropriate staff, and making sure all future correspondence gets to the right
place.

The CRM module has a email gateway for the synchronisation interface
between mails and Tiny ERP.""",
    "depends" : ["base"],
    "init_xml" : ["crm_data.xml"],
    "demo_xml" : ["crm_demo.xml"],
    "update_xml" : ["crm_view.xml", "crm_report.xml", "crm_wizard.xml", "crm_security.xml"],
    "active": False,
    "installable": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

