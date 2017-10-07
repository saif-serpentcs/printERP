# -*- coding: utf-'8' "-*-"
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#     (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = "mrp.bom"
    
    product_size_id = fields.Many2one('product.sizes', string="Size")
    sheet_id = fields.Many2one('product.template', string="Sheet", domain=[('is_sheet', '=', True)])
    
    

        
    @api.onchange('product_id')
    def onchange_product_size(self):
        context = dict(self._context) or {}
        print "\n\n\n context-----------", context
        product_size_ids = False
        if self.product_id:
            product_rec = self.env['product.product'].browse(self.product_id.id)
            print "\n\n\n product_rec-----------", product_rec
            product_size_ids = [product_size.id for product_size in product_rec.product_size_ids]
            print "----------product_size_ids", product_size_ids
        return {'domain' : {'product_size_id': [('id','in', product_size_ids)]}}

