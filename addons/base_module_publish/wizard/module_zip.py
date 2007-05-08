import wizard
import osv
import pooler
import os
import tools

from zipfile import PyZipFile, ZIP_DEFLATED
import StringIO
import base64

def _zippy(archive, fromurl, path):
	url = os.path.join(fromurl, path)
	if os.path.isdir(url):
		if path.split('/')[-1]=='.svn':
			return False
		for fname in os.listdir(url):
			_zippy(archive, fromurl, path and os.path.join(path, fname) or fname)
	else:
		if (path.split('.')[-1] not in ['py','pyo','pyc']) or (os.path.basename(path)=='__terp__.py'):
			print 'Adding', os.path.join(fromurl, path), 'as', path
			archive.write(os.path.join(fromurl, path), path)
	return True

def createzip(cr, uid, moduleid, context, b64enc=True):
	module_obj=pooler.get_pool(cr.dbname).get('ir.module.module')
	module_name = module_obj.browse(cr, uid, moduleid).name
	module_version = module_obj.browse(cr, uid, moduleid).latest_version

	ad = tools.config['addons_path']
	if os.path.isdir(os.path.join(ad,module_name)):
		archname = StringIO.StringIO('wb')
		archive = PyZipFile(archname, "w", ZIP_DEFLATED)
		archive.writepy(os.path.join(ad,module_name))
		_zippy(archive, ad, module_name)
		archive.close()
		val =archname.getvalue()
		archname.close()
	elif os.path.isfile(os.path.join(ad,module_name+'.zip')):
		val = file(os.path.join(ad,module_name+'.zip'),'rb').read()
	else:
		raise wizard.except_wizard('Error !', 'Could not find the module to export !')
	if b64enc:
		val =base64.encodestring(val)
	return {'module_file':val, 'module_filename': module_name+'-'+(module_version or 'x')+'.zip'}
