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
    "name" : "Manufacturing Resource Planning",
    "version" : "1.0",
    "author" : "Tiny",
    "website" : "http://tinyerp.com/module_mrp.html",
    "category" : "Generic Modules/Production",
    "depends" : ["stock", "hr", "purchase", "product"],
    "description": """
    This is the base module to manage the manufacturing process in Tiny ERP.

    Features:
    * Make to Stock / Make to Order (by line)
    * Multi-level BoMs, no limit
    * Multi-level routing, no limit
    * Routing and workcenter integrated with analytic accounting
    * Scheduler computation periodically / Just In Time module
    * Multi-pos, multi-warehouse
    * Different reordering policies
    * Cost method by product: standard price, average price
    * Easy analysis of troubles or needs
    * Very flexible

    It supports complete integration and planification of stockable goods,
    consumable of services. Services are completly integrated with the rest
    of the software. For instance, you can set up a sub-contracting service
    in a BoM to automatically purchase on order the assembly of your production.

    Reports provided by this module:
    * Bill of Material structure and components
    * Load forecast on workcenters
    * Print a production order
    * Stock forecasts
    """,
    "init_xml" : [],
    "demo_xml" : ["mrp_demo.xml","mrp_order_point.xml"],
    "update_xml" : [
        "mrp_workflow.xml", 
        "mrp_data.xml",
        "mrp_view.xml", 
        "mrp_wizard.xml", 
        "mrp_report.xml",
        "mrp_security.xml",
    ],
    "active": False,
    "installable": True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

