from odoo import api, fields, models, tools


class AppHideMenu(models.Model):
    _name = 'hide_app_menu'

    @api.multi
    def update_app_menu(self):
        self._cr.execute("""
          CREATE OR REPLACE FUNCTION public.Hide_Menu_App()
              RETURNS integer AS
                $BODY$ 
                    
                  BEGIN
                    UPDATE ir_ui_menu
                    SET active='f'
                    WHERE id=5;

                    UPDATE ir_ui_menu
                    SET active='f'
                    WHERE name = 'Complete Install';
                    RETURN 0;

                  END;
                    $BODY$
                    LANGUAGE plpgsql VOLATILE
                    COST 100;

                    SELECT * FROM Hide_Menu_App(); """)