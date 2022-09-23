# SINTKAS MEMBUAT  CLASS NEW MODEL OMO
# JANGAN LUPA KALO UDH COMPALTE CONNETING FILE PERSON KE __INIT__.PY
# DAN CONNTING SEMUA CLASSNYA KE SECURITY ACCESS
from odoo import api, fields, models

# CLASS PERSON
class Person(models.Model):
    _name = 'klasikmart.person'
    _description = 'FILE MODEL PERSON UNTUK KEBUTUHAN USER DI klasikMART'

    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')
    
    
