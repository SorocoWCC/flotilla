# -*- coding: utf-8 -*-
 
from openerp import models, fields, api
from openerp.exceptions import Warning
import time
import datetime
import dateutil
from datetime import date, timedelta, datetime
from dateutil import parser

# Clase Vehiculo
class vehiculo(models.Model):
    _name = "flotilla.vehiculo"
    _description = "Vehiculo"
    name = fields.Char(string='Placa', required=True)
    imagen_vehiculo = fields.Binary()
    motor = fields.Char(string='Motor')
    dueno_registral = fields.Char(string='Dueño Registral')
    rtv = fields.Selection([('Enero','Enero'), ('Febrero','Febrero'), ('Marzo','Marzo'), ('Abril','Abril'), ('Mayo','Mayo'), ('Junio','Junio'), ('Julio','Julio'), ('Agosto','Agosto'), ('Setiembre','Setiembre'), ('Octubre','Octubre'), ('Noviembre','Noviembre'), ('Diciembre','Diciembre')], string='RTV')
    chasis = fields.Char(string='Chasis')
    filtro_aceite = fields.Char(string='Filtro de Aceite')
    peso = fields.Integer(string='Peso')
    notas= fields.Text(string='Notas')
    periodo_cambio_aceite = fields.Integer(string='Perido Cambio de Aceite (dias)', required=True)
    gasto_ids = fields.One2many(comodel_name='gasto', inverse_name='vehiculo_id', string="Gastos",  readonly=True, domain=[('tipo_gasto', '=', 'aceite')])
    proximo_cambio_aceite = fields.Date(compute='_action_aceite', string="Proximo Cambio Aceite", readonly=True, store=True )
    _defaults = { 
    'periodo_cambio_aceite': 90,
    }

# Proximo Cambio de Aceite
    @api.one
    @api.depends('gasto_ids')
    def _action_aceite(self):
        contador = 0
        for gasto in self.gasto_ids :
          contador+= 1
          if contador == len(self.gasto_ids):
            fecha=datetime.strptime(str(gasto.fecha), '%Y-%m-%d')+timedelta(days=int(self.periodo_cambio_aceite))
            self.proximo_cambio_aceite = str(fecha)

# Clase Heredada Gasto
class gasto(models.Model):
    _name = 'gasto'
    _inherit = 'gasto'
    vehiculo_id = fields.Many2one(comodel_name='flotilla.vehiculo', string='Vehiculo')
    validar_vehiculo = fields.Float(compute='_validar_vehiculo', store=True, string="Validar Vehiculo")
    tipo_gasto = fields.Selection([('regular','Regular'), ('aceite','Cambio de Aceite'), ('repuesto','Repuestos'), ('reparacione','Reparaciones Mecánicas') ], string='Categoría')
    _defaults = { 
    'tipo_gasto': 'regular',
    }

# Validar id del vehiculo  
    @api.one
    @api.depends('name','vehiculo_id', 'tipo_gasto')
    def _validar_vehiculo(self):
        if self.tipo_gasto != "regular":
            if not self.vehiculo_id :   
                raise Warning ("Por Favor seleccione un vehículo")
