from odoo import api, fields, models


class KelompokBarang(models.Model):
    _name = 'klasikmart.kelompokbarang'
    _description = 'Ini adalah salah satu contoh model tabel Kelompok Barang!'

    #INI TEKS YG LAMA HARUS ISI MANUAL DI NAMA KELOMPOK
    #name = fields.Char(string='Nama Kelompok') 
    #---------------------------------------------
    #MEMBUAT SELECTION/OTOMATIS DI KELOMPOK BARANG DENGAN SINTAKS OFSE
    # Supaya tidak mengahasilan ouput  ganda 
    name = fields.Selection([
        ('rock', 'Rock'),('reggae','Reggae'),('pop','Pop')
    ], string='Jenis Genre')
    #-------------------------------------------------

    #INI TEKS YG LAMA HARUS ISI MANUAL DI KODE KELOMPOK
    #kode_kelompok = fields.Char(string='Kode Kelompok')
    #--------------------------------------------------
    # MEMBUAT COMPUTE ONCHANGE KODE KELOMPOK TO NAMA KELOMPOK DENGAN SINTAKS OFCO,
    #JADI TUH SEKALI GANTI NYESUAIN SAMA NAMA KELOMPOK DI FORM
    kode_kelompok = fields.Char(onchange='_compute_kode_kelompok', string='Kode Genre')
    @api.onchange('name') # name karna nyesuain dengan nama kelompok diatas
    def _compute_kode_kelompok(self):
        if (self.name == 'rock'): # == isi dengan key yg ada di nama kelompok diatas
            self.kode_kelompok = 'metalhead'
        elif (self.name == 'reggae'):
            self.kode_kelompok = 'rastaman'
        elif (self.name == 'pop'):
            self.kode_kelompok = 'populer'

    kode_rak = fields.Char(string='Nomer Rak')
    #INI SINTAKS MAKE ONE TO MANY (OFO)
    barang_ids = fields.One2many(comodel_name='klasikmart.barang', #INI NGAMBIL MODULENYA DI CLASS BARANG FILE BARANG.PY  
                                inverse_name='kelompokbarang_id', # MASIH SAMA DIATAS DAN ARAHIN KE KEY MTO BARANG 
                                      string='Daftar Album')
            
    #SCRIPT HITUNG JML ITEM BARANG MENGGUNAKAN OFCO,
    jml_item = fields.Char(compute='_compute_jml_item', string='Jumlah Item')
    
    @api.depends('barang_ids') # NYESUAIIN NAME BARANG_IDS di dalamnynya
    def _compute_jml_item(self):
        for rec in self:
            a = self.env['klasikmart.barang'].search([('kelompokbarang_id','=', rec.id)]).mapped('name')
            b = len(a)
            rec.jml_item = b
            rec.daftar = a
    
    # MEMBUAT DESK KELOMPOK BARANG APA SAJA ISINYA, DENGAN SINTAKS OFCHAR
    daftar = fields.Char(string='Daftar Isi')