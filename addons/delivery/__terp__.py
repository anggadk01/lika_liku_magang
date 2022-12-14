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
    "name" : "Carriers and deliveries",
    "version" : "1.0",
    "author" : "Tiny",
    "category" : "Generic Modules/Sales & Purchases",
    "description": "Allows to add delivery methods in sales order and packings. You can define your own carrier and delivery grids for prices. When creating invoices from pickings, Tiny ERP is able to add and compute the shipping line.",
    "depends" : ["sale","purchase", "stock",],
    "init_xml" : ["delivery_data.xml"],
    "demo_xml" : ["delivery_demo.xml"],
    "update_xml" : ["delivery_view.xml","delivery_wizard.xml"],
    "active": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

