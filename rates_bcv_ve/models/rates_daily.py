import requests
from bs4 import BeautifulSoup
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class RatesDaily(models.Model):
    _name = 'rates.daily'
    _description = 'Tasas Diarias BCV'
    _order = 'date desc'

    name = fields.Char(string='Referencia',
                       compute='_compute_name', store=True)
    date = fields.Date(string='Fecha de Consulta',
                       default=fields.Date.context_today, required=True)
    currency_name = fields.Selection([
        ('USD', 'Dólar (USD)'),
        ('EUR', 'Euro (EUR)')
    ], string='Moneda', required=True)
    rate_value = fields.Float(
        string='Valor de la Tasa', digits=(12, 4), required=True)

    @api.depends('date', 'currency_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.currency_name} - {record.date}"

    @api.model
    def action_sync_bcv(self):
        """Método principal de Scraping"""
        url = 'https://www.bcv.org.ve/'
        try:
            # Bypass de verificación SSL si el sitio del BCV tiene certificados vencidos
            response = requests.get(url, verify=False, timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # IDs específicos que usa la web del BCV para las tasas
            currencies = {
                'USD': 'dolar',
                'EUR': 'euro'
            }

            for code, html_id in currencies.items():
                element = soup.find('div', id=html_id)
                if element:
                    # Extraer el valor y limpiar (cambiar coma por punto para float)
                    val_str = element.find(
                        'strong').text.strip().replace(',', '.')
                    rate = float(val_str)

                    # Guardar en nuestra tabla
                    self.create({
                        'currency_name': code,
                        'rate_value': rate,
                        'date': fields.Date.context_today(self)
                    })

            return True
        except Exception as e:
            _logger.error(f"Error en Scraping BCV: {str(e)}")
            raise UserError(
                _("No se pudo conectar con el BCV. Intente más tarde."))
