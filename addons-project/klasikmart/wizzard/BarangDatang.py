from odoo import api, fields, models


class BarangDatang(models.TransientModel):
    _name = 'klasikmart.barangdatang'

    barang_id = fields.Many2one(
        comodel_name='klasikmart.barang',
        string='Jenis Album',
        required=True)


    jumlah = fields.Integer(
        string='Jumlah',
        required=False)


    # KORELASI DENGAN BUTTON INPUT BARANG  
    def button_barang_datang(self):
        for rec in self:
            # SINGKRONISASI ADD BARANG DATANG KE STOK BARANG
            self.env['klasikmart.barang'] \
                .search([('id', '=', rec.barang_id.id)]) \
                .write({'stok': rec.barang_id.stok + rec.jumlah})