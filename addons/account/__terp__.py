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
    "name" : "Accounting and financial management",
    "version" : "1.0",
    "depends" : ["product", "base"],
    "author" : "Tiny",
    "description": """Financial and accounting module that covers:
    General accounting
    Cost / Analytic accounting
    Third party accounting
    Taxes management
    Budgets
    """,
    "website" : "http://tinyerp.com/module_account.html",
    "category" : "Generic Modules/Accounting",
    "init_xml" : [
        
    ],
    "demo_xml" : [
        "account_demo.xml",
        "project/project_demo.xml",
        "project/analytic_account_demo.xml",
        "account_unit_test.xml",
    ],
    "update_xml" : [
        "account_wizard.xml",
        "account_view.xml",
        "account_end_fy.xml",
        "account_invoice_view.xml",
        "account_report.xml",
        "partner_view.xml",
        "data/account_invoice.xml",
        "data/account_data1.xml",
        "data/account_minimal.xml",
        "data/account_data2.xml",
        "account_invoice_workflow.xml",
        "project/project_view.xml",
        "project/project_report.xml",
        "product_data.xml",
        "product_view.xml",
        "account_security.xml",
        "project/project_security.xml", 
        "account_assert_test.xml",
    ],
    "translations" : {
        "fr": "i18n/french_fr.csv"
    },
    "active": False,
    "installable": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

