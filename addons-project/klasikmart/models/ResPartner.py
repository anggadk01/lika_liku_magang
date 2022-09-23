from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Ini adalah salah satu contoh model tabel inherit ResPartner!'

    is_konsumen = fields.Boolean(string='Is Konsumen')
    
    

    
