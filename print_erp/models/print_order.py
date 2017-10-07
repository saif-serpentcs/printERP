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
import odoo.addons.decimal_precision as dp


class PrintOrder(models.Model):

    _name = "print.order"
    _description = "Print Order"
    _order = 'date_order asc'
    
    @api.multi
    def confrim_sale_order(self):
        order_line_ids = []
        sale_order_obj = self.env['sale.order']
        for rec in self:
            if rec.sale_done:
                raise ValidationError(_('Sale Order are alrady Generated!'))
            if not rec.partner_id:
                raise ValidationError(_('Partner/Customer is not defind!'))
            for line in rec.print_order_ids:
                order_line_ids.append((0, 0, {'product_id': line.product_id.id, 
                                              'name': line.name,
                                              'product_uom_qty': line.product_uom_qty,
                                              'product_size_id': line.product_size_id.id,
                                              'sheet_id': line.sheet_id.id,
                                              'price_unit': line.price_unit,
                                              'use_sheet': line.use_sheet,
                                              'westage': line.westage}))
            sale_order_id = sale_order_obj.create({'partner_id': rec.partner_id.id,
                                                   'order_line':order_line_ids,
                                                   'state' : 'sale'})
            rec.write({'sale_order_id': sale_order_id.id,
                       'state':'sale_order',
                       'sale_done': True,})
        return {'name': _('Sale Order'),
                'context': self._context,
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(self.env.ref('sale.view_order_form').id, 'form')],
                'view_id': self.env.ref('sale.view_quotation_tree').id,
                'res_model': 'sale.order',
                'type': 'ir.actions.act_window',
                'res_id': sale_order_id and sale_order_id.id or False}
    
    @api.multi
    def re_sale_order(self):
        order_line_ids = []
        sale_order_obj = self.env['sale.order']
        for rec in self:
            rec.copy()
            if not rec.partner_id:
                raise ValidationError(_('Partner/Customer is not defind!'))
            for line in rec.print_order_ids:
                order_line_ids.append((0, 0, {'product_id': line.product_id.id, 
                                              'name': line.name,
                                              'product_uom_qty': line.product_uom_qty,
                                              'product_size_id': line.product_size_id.id,
                                              'sheet_id': line.sheet_id.id,
                                              'price_unit': line.price_unit}))
            sale_order_id = sale_order_obj.create({'partner_id': rec.partner_id.id,
                                                   'order_line':order_line_ids,
                                                   'state' : 'sale'})
            rec.write({'sale_order_id': sale_order_id.id,
                       'sale_done': True,})
        return {'name': _('Sale Order'),
                'context': self._context,
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(self.env.ref('sale.view_order_form').id, 'form')],
                'view_id': self.env.ref('sale.view_quotation_tree').id,
                'res_model': 'sale.order',
                'type': 'ir.actions.act_window',
                'res_id': sale_order_id and sale_order_id.id or False}
    
    @api.multi
    def open_order(self):
        for rec in self:
            return {'name': _('Sale Order'),
                    'context': self._context,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'views': [(self.env.ref('sale.view_order_form').id, 'form')],
                    'view_id': self.env.ref('sale.view_quotation_tree').id,
                    'res_model': 'sale.order',
                    'type': 'ir.actions.act_window',
                    'res_id': rec.sale_order_id and rec.sale_order_id.id or False}
    
    @api.multi
    def sent_order(self):
        local_context = self.env.context.copy()
        for rec in self:
            if not rec.partner_id:
                raise ValidationError(_('Customer does not exist!'))
            template = self.env.ref('print_erp.email_template_order_created', False)
            if not template:
                raise UserError(_('The Forward Email Template is not in the database'))
            local_context['partner_id'] = rec.partner_id
            if rec.partner_id and rec.partner_id.email and template:
                mail_id = template.with_context(local_context).send_mail(rec.id, force_send=True)
            return rec.write({'state': 'confirm'})
        return True
    
    @api.depends('print_order_ids.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the Order.
        """
        amount_untaxed = 0.0
        for order in self:
            for line in order.print_order_ids:
                amount_untaxed += line.price_total
            order.update({
                'amount_total': amount_untaxed
            })
    
#     def create(self, cr, uid, vals, context=None):
#         if context is None:
#             context = {}
#         if vals is None:
#             vals = {}
#         email_template_obj = self.pool.get('email.template')
#         if vals.get('partner_id', False):
#             partner_rec = self.pool.get('res.partner').browse(cr, uid, vals.get('partner_id'), context=context)
#             template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fmis_contract', 'email_template_momp_invoice')[1]
#         res = super(account_invoice, self).create(cr, uid, vals, context=context)
#         context.update({'from_create': True})
#         if partner_rec and partner_rec.email and template_id:
#             email_template_obj.send_mail(cr, uid, template_id, res, force_send=True, context=context)
#         return res

    crm_lead_id = fields.Many2one('crm.lead', string='Lead', ondelete='cascade')
    name = fields.Char(related='crm_lead_id.name', string="name", readonly=True)
    partner_id = fields.Many2one(related='crm_lead_id.partner_id', comodel_name='res.partner', string='Customer', track_visibility='onchange', 
                                 index=True, readonly=True, store=True)
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False, default=fields.Datetime.now)
    confirmation_date = fields.Datetime(string='Confirmation Date', readonly=True, index=True, help="Date on which the sale order is confirmed.", oldname="date_confirm")
    image_medium = fields.Binary(related='partner_id.image_medium', string='Medium-sized photo', readonly=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(related='crm_lead_id.company_id', string='Company', store=True, readonly=True)
    print_order_ids = fields.One2many('print.order.line', 'print_order_id', string='Print Order lines', copy=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    amount_total = fields.Float(string='Total', compute='_amount_all', readonly=True, track_visibility='always')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('print.order'))
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True, required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('sale_order', 'Sale Order'),
                              ('rejected', 'Rejected')], string="Stage", default='draft')
    print_attachment_ids = fields.One2many('ir.attachment', 'print_ordre_id', string='Attachments')
    note = fields.Text(string = 'Notes')
    sale_done = fields.Boolean('Done Sale Order')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    reject_reason = fields.Text(string='Reason', readonly=True)
    end_date = fields.Date(string='End Date', readonly=True)
    
    @api.multi
    def action_submit_print_order_form(self):
        for rec in self:
            if not rec.crm_lead_id.print_order_id:
                rec.crm_lead_id.write({'print_order_id': rec.id})
        return True


class PrintOrderLine(models.Model):

    _name = "print.order.line"
    _description = "Print Order Line"
    
    @api.multi
    def _get_default_category_id(self):
        category = self.env.ref('product.product_category_all', raise_if_not_found=False)
        return category and category.type == 'normal' and category.id or False
    
    @api.depends('product_uom_qty', 'price_unit',)
    def _compute_amount(self):
        """
        Compute the amounts of the Print line.
        """
        for line in self:
            price = line.price_unit * line.product_uom_qty
            line.update({
                'price_total': price,
            })
    
    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        for rec in self:
            if rec.product_id:
                rec.name = rec.product_id.name_get()[0][1]
                if rec.product_id.description_sale:
                    rec.name += '\n' + product.description_sale
    
    @api.one
    @api.depends('product_id', 'product_size_id', 'sheet_id','product_uom_qty')
    def _cal_sheet_westage(self):
        '''Calculate the '''
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
    
    print_order_id = fields.Many2one('print.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    sequence = fields.Integer(string='Sequence', default=10)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=True)
    image_medium = fields.Binary(related='product_id.image_medium', string='Medium-sized photo', readonly=True)
    product_categ_id = fields.Many2one('product.category', 'Internal Category',
        change_default=True, default=_get_default_category_id, domain="[('type','=','normal')]",
        required=True, help="Select category for the current product")
    
    product_uom_qty = fields.Float(string='Quantity', required=True, default=100.0)
    name = fields.Char(string='Description', required=True)
    product_size_id = fields.Many2one('product.sizes', string="Size")
    sheet_id = fields.Many2one('product.template', string="Sheet", domain=[('is_sheet', '=', True)])
    customized_size = fields.Boolean('Customized Size')
    height = fields.Float(string='Height')
    weight = fields.Float(string='Weight')
    use_sheet = fields.Integer(compute='_cal_sheet_westage', string='Used Sheet', readonly=True)
    westage = fields.Integer(compute='_cal_sheet_westage', string='Westage', readonly=True)
    price_unit = fields.Float('Public Price', related='product_id.lst_price', digits=dp.get_precision('Product Price'))
    currency_id = fields.Many2one(related='print_order_id.currency_id', store=True, string='Currency', readonly=True)
    company_id = fields.Many2one(related='print_order_id.company_id', string='Company', store=True, readonly=True)
    price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
    note = fields.Text(string = 'Notes')
    

class ir_attachment(models.Model):
    _inherit = 'ir.attachment'
    
    print_ordre_id = fields.Many2one('print.order', string='Print Order', ondelete='cascade')
    