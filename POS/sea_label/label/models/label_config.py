from odoo import models, fields, api, _


class LabelMain(models.Model):
    _name = 'label.brand'
    _rec_name = 'brand_name'

    _description = 'Configured Label Brands'

    brand_name = fields.Char('Name', size=64, index=True)
    label_config_ids = fields.One2many('label.config', 'label_main_id',
                                       'Label Config')


class LabelConfig(models.Model):
    _name = 'label.config'

    _description = 'Configuration for label'

    name = fields.Char("Name", size=64, required=True, index=True)
    height = fields.Float("Height (in mm)", required=True)
    width = fields.Float("Width (in mm)", required=True)
    top_margin = fields.Float("Top Margin (in mm)", default=0.0)
    bottom_margin = fields.Float("Bottom Margin  (in mm)", default=0.0)
    left_margin = fields.Float("Left Margin (in mm)", default=0.0)
    right_margin = fields.Float("Right Margin (in mm)", default=0.0)
    cell_spacing = fields.Float("Cell Spacing", default=1.0)
    label_main_id = fields.Many2one('label.brand', 'Label')

class address(models.Model):
    _inherit = 'product.template'
    # _name = 'company.address'

    partner_id = fields.Many2one('res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('product.template'))
    mfg_date = fields.Date(string="MFG")
    exp_date = fields.Date(string="Expiry")
    # This code has been reviewed, above created fields are working fine in front end as required.