from odoo import api, fields, models


class Konsumen(models.Model):
    _inherit = 'res.partner'
    _description = 'Ini adalah salah satu contoh model tabel Barang!'
    poin = fields.Integer(string='Poin')
    level = fields.Char(string='Level')
    