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
import wizard
import osv
import pooler
import os
import tools

from zipfile import PyZipFile, ZIP_DEFLATED
import StringIO
import base64

def _zippy(archive, fromurl, path, src=True):
    url = os.path.join(fromurl, path)
    if os.path.isdir(url):
        if path.split('/')[-1].startswith('.'):
            return False
        for fname in os.listdir(url):
            _zippy(archive, fromurl, path and os.path.join(path, fname) or fname, src=src)
    else:
        if src:
            exclude = ['pyo', 'pyc']
        else:
            exclude = ['py','pyo','pyc']
        if (path.split('.')[-1] not in exclude) or (os.path.basename(path)=='__terp__.py'):
            archive.write(os.path.join(fromurl, path), path)
    return True

def createzip(cr, uid, moduleid, context, b64enc=True, src=True):
    pool = pooler.get_pool(cr.dbname)
    module_obj = pool.get('ir.module.module')

    module = module_obj.browse(cr, uid, moduleid)

    if module.state != 'installed':
        raise wizard.except_wizard(_('Error'),
                _('Can not export module that is not installed!'))

    ad = tools.config['addons_path']
    if os.path.isdir(os.path.join(ad, module.name)):
        archname = StringIO.StringIO('wb')
        archive = PyZipFile(archname, "w", ZIP_DEFLATED)
        archive.writepy(os.path.join(ad, module.name))
        _zippy(archive, ad, module.name, src=src)
        archive.close()
        val =archname.getvalue()
        archname.close()
    elif os.path.isfile(os.path.join(ad, module.name + '.zip')):
        val = file(os.path.join(ad, module.name + '.zip'), 'rb').read()
    else:
        raise wizard.except_wizard(_('Error'), _('Could not find the module to export!'))
    if b64enc:
        val =base64.encodestring(val)
    return {'module_file':val, 'module_filename': module.name + '-' + \
            (module.installed_version or '0') + '.zip'}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

