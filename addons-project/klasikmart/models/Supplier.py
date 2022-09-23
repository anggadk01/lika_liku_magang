from odoo import api, fields, models


class Supplier(models.Model):
    _name = 'klasikmart.supplier'
    _description = 'Ini adalah salah satu contoh model tabel Supplier!'

    name = fields.Char(string='Nama Perusahaan')
    alamat = fields.Char(string='Alamat')
    no_telp = fields.Char(string='No. Telepon')
    # INI SINTAKS M2M ANTARA SUPPLIER DENGAN BARANG.PY
    barang_id = fields.Many2many(comodel_name='klasikmart.barang', string='Barang')
    
    
    
