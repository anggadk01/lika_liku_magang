from odoo import api, fields, models


class Barang(models.Model):
    _name = 'klasikmart.barang'
    _description = 'Ini adalah salah satu contoh model tabel Barang!'

    name = fields.Char(string='Band - Album')
    harga_beli = fields.Integer(string='Harga Modal',required=True)
    harga_jual = fields.Integer(string='Harga Jual', required=True)
    image = fields.Image(string="Image")
    list_lagu = fields.Char(string='\n List Lagu')
    kelompokbarang_id = fields.Many2one(comodel_name='klasikmart.kelompokbarang',
                                              string='Jenis Genre',
                                            ondelete='cascade')
    
    # INI SINTAKS M2M ANTARA SUPPLIER DENGAN BARANG.PY
    supplier_id = fields.Many2many(comodel_name='klasikmart.supplier', string='Supplier')
    stok = fields.Integer(string='Stok Album')
    
    
    
    
