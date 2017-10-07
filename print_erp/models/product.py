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


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_sheet = fields.Boolean('Is Sheet')
    sheet_type = fields.Selection([('Paper', 'Paper'), 
                                   ('Card', 'Card')], 'Sheet Type', default='Paper')
    color_name = fields.Selection([('Cyan', 'Cyan'), 
                                   ('Gray', 'Gray'), 
                                   ('Green', 'Green'), 
                                   ('White', 'White'), 
                                   ('Yellow', 'Yellow')], 'Color Name', default='White')
    active = fields.Boolean(string='Active', default=True)
    height = fields.Float(string='Height')
    weight = fields.Float(string='Weight')



class ProductSizes(models.Model):
    _name = 'product.sizes'
    _description = 'Product Sizes'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        context = dict(self._context) or {}
        if args is None:
            args = []
        if 'from_print_order' in context:
            product_rec = self.env['product.product'].browse(context.get('product_id'))
            product_size_ids = [product_size.id for product_size in product_rec.product_size_ids]
            args.append(('id', 'in', product_size_ids))
        return super(ProductSizes, self)._search(args=args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)

    image_medium = fields.Binary(string="Big-sized image")
    name = fields.Char(string='Name', index=True, required=True, translate=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active', default=True)
    height = fields.Float(string='Height', required=True)
    weight = fields.Float(string='Weight', required=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    product_size_ids = fields.Many2many('product.sizes', string="Product Sizes")
    sheet_ids = fields.Many2many('product.product', 'product_sheet_rel', 'product_id', 'sheet_id', string='Sheet', domain=[('is_sheet', '=', True)])
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        context = dict(self._context) or {}
        if args is None:
            args = []
        if 'from_print_order' in context:
            product_rec = self.browse(context.get('product_id'))
            product_sheet_ids = [product_size.id for product_size in product_rec.sheet_ids]
            args.append(('id', 'in', product_sheet_ids))
        return super(ProductProduct, self)._search(args=args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)


# class SheetSizes(models.Model):
#     _name = 'sheet.sizes'
#     _description = 'Sheet Sizes'
# 
#     name = fields.Char(string='Name', index=True, required=True, translate=True)
#     code = fields.Char(string='Code')
#     active = fields.Boolean(string='Active', default=True)
#     height = fields.Float(string='Height', required=True)
#     weight = fields.Float(string='Weight', required=True)

