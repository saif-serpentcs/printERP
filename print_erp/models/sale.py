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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    @api.one
    @api.depends('product_id', 'product_size_id', 'sheet_id','product_uom_qty')
    def _cal_sheet_westage(self):
        self.use_sheet = product_size = sheet_size = one_sheet_qty = use_sheet = 0.0
        if self.product_id and self.product_size_id and self.sheet_id:
            if self.product_size_id.height and self.product_size_id.weight:
                product_size = self.product_size_id.height * self.product_size_id.weight
            if self.sheet_id.height and self.sheet_id.weight:
                sheet_size = self.sheet_id.height * self.sheet_id.weight
            if product_size and sheet_size:
                one_sheet_qty = sheet_size / product_size
            if one_sheet_qty and self.product_uom_qty:
                use_sheet = self.product_uom_qty / int(one_sheet_qty)
            self.use_sheet = use_sheet
            #westage
            if "." in str(one_sheet_qty):
                westage_per_sheet = "." + str(round(one_sheet_qty, 2)).split(".")[-1]
                self.westage = use_sheet * float(westage_per_sheet)
    
    @api.multi
    def _get_default_category_id(self):
        category = self.env.ref('product.product_category_all', raise_if_not_found=False)
        return category and category.type == 'normal' and category.id or False
    
    product_categ_id = fields.Many2one('product.category', 'Product', change_default=True, default=_get_default_category_id, domain="[('type','=','normal')]",
        required=True, help="Select category for the current product")
    
    product_size_id = fields.Many2one('product.sizes', string="Size")
    sheet_id = fields.Many2one('product.template', string="Sheet", domain=[('is_sheet', '=', True)])
    customized_size = fields.Boolean('Customized Size')
    height = fields.Float(string='Height')
    weight = fields.Float(string='Weight')
    use_sheet = fields.Integer(string='Used Sheet', readonly=True)
    westage = fields.Integer(string='Westage', readonly=True)
