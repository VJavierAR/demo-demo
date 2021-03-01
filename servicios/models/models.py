# -*- coding: utf-8 -*-

from odoo import _, models, fields, api, tools
from email.utils import formataddr
from odoo.exceptions import UserError
from odoo import exceptions, _
import logging, ast
import datetime, time
_logger = logging.getLogger(__name__)

def get_plazo():
    year_list = []
    for i in range(1, 100):
       year_list.append((i, str(i)))
    return year_list

class contratos(models.Model):
    _name = "contrato"
    _description = 'Contratos'
    
    name = fields.Char(string="Nombre")
    #servicio = fields.One2many('servicios', 'contrato',string="Servicio")
    ci = fields.Binary(string="carta de intención")
    c = fields.Binary(string="contrato")
    ac = fields.Binary(string="Acta constitutiva")
    cs = fields.Binary(string="constancia del sat")
    idal = fields.Binary(string="id apoderado legal")
    penalizaciones = fields.One2many('penalizaciones','contrato',string="Penalizaciones")

    dividirLocalidades = fields.Boolean(string="Dividir Localidades", default=False)
    dividirServicios = fields.Boolean(string="Dividir Servicios", default=False)
    dividirExcedentes = fields.Boolean(string="Dividir Excedentes", default=False)
    mostrarUbicaciones = fields.Boolean(string="Mostrar Ubicaciones", default=False)
    
    
    
    cliente = fields.Many2one('res.partner', string='Cliente')
    idtmpp = fields.Char(string="idTMPp")
    tipoDeCliente = fields.Selection([('A','A'),('B','B'),('C','C'),('VIP','VIP'),('OTRO','Otro')], default='A', string="Tipo de cliente")
    mesaDeAyudaPropia = fields.Boolean(string="Mesa de ayuda propia", default=False)
    
    ejecutivoDeCuenta = fields.Many2one('hr.employee', string='Ejecutivo de cuenta')
    vendedor = fields.Many2one('hr.employee', string="Vendedor")
    
    tipoDeContrato = fields.Selection([('ARRENDAMIENTO','Arrendamiento'),('DEMOSTRACION','Demostración'),('OTRO','Otro')], default='ARRENDAMIENTO', string="Tipo de contrato")
    vigenciaDelContrato = fields.Selection([('INDEFINIDO','Indefinido'),('12','12'),('18','18'),('24','24'),('36','36'),('OTRO','Otro')], default='12', string="Vigencia del contrato (meses)")
    fechaDeInicioDeContrato = fields.Datetime(string = 'Fecha de inicio de contrato',track_visibility='onchange')
    fechaDeFinDeContrato = fields.Datetime(string = 'Fecha de finalización de contrato',track_visibility='onchange')
    fechaDeFirmaDeContrato = fields.Datetime(string = 'Fecha firma de contrato',track_visibility='onchange')
    ordenDeCompra = fields.Text(string="URL de orden de compra",track_visibility='onchange')
    instruccionesOrdenDeCompra = fields.Text(string="Instrucciones de orden de compra",track_visibility='onchange')
    
    tonerGenerico = fields.Boolean(string="Tóner genérico", default=False)
    equiposNuevos = fields.Boolean(string="Equipos nuevos", default=False)
    periodicidad = fields.Selection([('MENSUAL','Mensual'),('BIMESTRAL','Bimestral'),('TRIMESTRAL','Trimestral'),('CUATRIMESTRAL','Cuatrimestral'),('SEMESTRAL','Semestral'),('ANUAL','Anual'),('CONTRATO','Contrato')], default='BIMESTRAL', string="Periodicidad")
    idTechraRef = fields.Integer(string="ID techra ref")

    adjuntos = fields.Selection([("APODERADO_LEGAL_ID","Id de apoderado legal"),("CONSTANCIA_SAT","constancia del SAT"),("ACTACONSTITUTIVA","Acta constitutiva"),("CONTRATO","Contrato"),('CONTRATO DEBIDAMENTE REQUISITADO Y FIRMADO','Contrato debidamente requisitado y firmado'),('CARTA DE INTENCION','Carta de intención')], default='CONTRATO DEBIDAMENTE REQUISITADO Y FIRMADO', string="Se adjunta")
    documentacion = fields.Many2many('ir.attachment', string="Documentación")

    rfcCliente = fields.Many2one('hr.employee',string="RFC Del cliente",track_visibility='onchange')
    
    #------------------------------------------------------------------------------------------
    #Contrato

    formaDePago = fields.Selection([('1','01 - Efectivo') ,('2','02 - Cheque nominativo') ,('3','03 - Transferencia electrónica de fondos') ,('4','04 - Tarjeta de crédito') ,('5','05 - Monedero electrónico') ,('6','06 - Dinero electrónico') ,('7','08 - Vales de despensa') ,('8','12 - Dación en pago') ,('9','13 - Pago por subrogación') ,('10','14 - Pago por consignación') ,('11','15 - Condonación') ,('12','17 - Compensación') ,('13','23 - Novación') ,('14','24 - Confusión') ,('15','25 - Remisión de deuda') ,('16','26 - Prescripción o caducidad') ,('17','27 - A satisfacción del acreedor') ,('18','28 - Tarjeta de debito') ,('19','29 - Tarjeta de servicios') ,('20','30 - Aplicación de anticipos') ,('22','99 - Por definir')], string = "Forma de pago",track_visibility='onchange',default='22')

    #banco = fields.Selection([(1, ' - BNM840515VB1'), (2, ' - 12799.44'), (3, ' - SIN9412025I4'), (4, 'BAJIO - BBA940707IE1'), (5, 'BANAM - BNM840515VB1'), (6, 'BANAMEX - BNM840515VB1'), (7, 'BANAMEX - '), (8, 'BANAMEX - BNM840515VB'), (9, 'BANBAJIO - BBA940707IE1'), (10, 'BANCA MIFEL - BMI9312038R3'), (11, 'BANCO AZTECA - BAI0205236Y8'), (12, 'BANCO BASE - BBS110906HD3'), (13, 'BANCO DEL BAJ�O - BBA940707IE1'), (14, 'BANCO DEL BAJIO SA - BBA940707IE1'), (15, 'BANCO J.P. MORGAN S.A. - BJP-950104-LJ'), (16, 'BANCO J.P. MORGAN S.A. - BJP950104LJ5'), (17, 'BANCO J.P.MORGAN SA - BJP950104LJ5'), (18, 'Banco Mercantil del Norte - BMN930209927'), (19, 'BANCO MERCANTIL DEL NORTE - BMN930209927'), (20, 'BANCO MERCANTIL DEL NORTE S.A. - BMN930209-927'), (21, 'BANCO MERCANTIL DEL NORTE S.A. - BMN930209927'), (22, 'BANCO MULTIVA, SA - BMI061005NY5'), (23, 'BANCO REGIONAL DE MONTERREY S.A. - BRM940216EQ6'), (24, 'BANCO SANTANDER - BSM970519DU8'), (25, 'BANCO SANTANDER (MEXICO) S.A., INSTITUCION DE BANC - BSM970519DU8'), (26, 'BANCO SANTANDER (MEXICO) SA - BSM970519DU8'), (27, 'BANCO VE POR MAS - BVM951002LX0'), (28, 'BANCOMER - BBA830831LJ2'), (29, 'BANCOMER - '), (30, 'BANCONER - BBA830831LJ2'), (31, 'BANK OF AMERICA MEXICO - '), (32, 'BANK OF AMERICA MEXICO - BAM9504035J2'), (33, 'BANORTE - EOP510101UA4'), (34, 'BANORTE - BMN930209927'), (35, 'BANORTE - '), (36, 'BANORTE - BMN930299277'), (37, 'BANORTE - BMN930209 927'), (38, 'BANREGIO - BRM940216EQ6'), (39, 'BBVA BANCOMER - BBA830831LJ2'), (40, 'BBVA Bancomer - BBA830831LJ2'), (41, 'BBVA BANCOMER - '), (42, 'BBVA Bancomer, S.A. - BBA830831LJ2'), (43, 'CI BANCO - BCI001030ECA'), (44, 'CI BANCO - CIB850918BN'), (45, 'CI BANCO - BNY080206UR9'), (46, 'CITI BANAMEX - BNM840515VB1'), (47, 'HSBC - HMI950125KG8'), (48, 'HSBC - '), (49, 'HSBC - HSBC046722'), (50, 'HSBC . - HMI950125KG8'), (51, 'HSBC MEXICO S.A. - HMI-950125KG8'), (52, 'HSBC MEXICO S.A. - HMI950125KG8'), (53, 'HSBC MEXICO S.A. - ASC960408K10'), (54, 'HSBC MEXICO S.A. - '), (55, 'INBURSA - BII931004P61'), (56, 'INBURSA - FCS890710CW5'), (57, 'INVERLAT - SIN9412025I4'), (58, 'J P MORGAN - BJP950104LJ5'), (59, 'J P MORGAN - XEXX010101000'), (60, 'MONEX - BMI9704113PA'), (61, 'MULTIVA - BMI061005NY5'), (62, 'MULTIVA - BMI061005NYS'), (63, 'SANTANDER - BSM970519DU8'), (64, 'SANTANDER - XEXX010101000'), (65, 'SANTANDER - SIN9412025I4'), (66, 'SANTANDER - BSM970519DUB'), (67, 'SANTANDER - '), (68, 'SANTANDER - BMN930299277'), (69, 'SCOTIABANK - SIN9412025I4'), (70, 'SCOTIABANK INVERLAT SA - SIN9412025I4'), (71, 'Scotiabank Inverlat, S.A. - SIN9412025I4'), (72, 'SCOTIANBANK INVERLAT - SIN9412025I4')], string = "Banco",track_visibility='onchange')

    #cuentaBancaria  = fields.Selection([('24','BAJIO - 9777600201 - MON NAC') ,('19','BANAMEX - 002180418300272792 - MONEDA NAC') ,('12','BANAMEX - 002180700725697152 - CHEQUES M.') ,('16','CI BANCO - 0001120336 - MONEDA NAC') ,('17','MULTIVA - 0004738918 - MONEDA NAC')], string = "Cuenta bancaria definida",track_visibility='onchange')
    formaDePagoComplemento = fields.Selection([('3','01 - Efectivo') ,('2','02 - Cheque nominativo') ,('1','03 - Transferencia electrónica de fondos') ,('4','04 - Tarjeta de crédito') ,('7','05 - Monedero electrónico') ,('10','06 - Dinero electrónico') ,('11','08 - Vales de despensa') ,('12','12 - Dación en pago') ,('13','13 - Pago por subrogación') ,('14','14 - Pago por consignación') ,('15','15 - Condonación') ,('16','17 - Compensación') ,('17','23 - Novación') ,('18','24 - Confusión') ,('19','25 - Remisión de deuda') ,('20','26 - Prescripción o caducidad') ,('21','27 - A satisfacción del acreedor') ,('5','28 - Tarjeta de debito') ,('6','29 - Tarjeta de servicios') ,('9','30 - Aplicación de anticipos') ,('22','30 - Aplicación de anticipos') ,('8','99 - Por definir')], string = "Forma de pago complemento",track_visibility='onchange')

    metodPago = fields.Selection([('6','PPD Pago en parcialidades o diferido') ,('5','PUE Pago en una sola exhibición')], string = "Método de pago",track_visibility='onchange',default='6')
    numCuenta = fields.Integer(string="Número Cuenta",track_visibility='onchange')
    numCuentaT = fields.Text(string="Número Cuenta",track_visibility='onchange')

    razonSocial  = fields.Char(string = "Razón Social interna",track_visibility='onchange', default=lambda self: self.env.user.razonSocial)

    usoCFDI = fields.Selection([('12','D01 Honorarios médicos, dentales y gastos hospitalarios.') ,('13','D02 Gastos médicos por incapacidad o discapacidad') ,('14','D03 Gastos funerales.') ,('15','D04 Donativos.') ,('16','D05 Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación).') ,('17','D06 Aportaciones voluntarias al SAR.') ,('18','D07 Primas por seguros de gastos médicos.') ,('19','D08 Gastos de transportación escolar obligatoria.') ,('20','D09 Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.') ,('21','D10 Pagos por servicios educativos (colegiaturas)') ,('1','G01 Adquisición de mercancias') ,('2','G02 Devoluciones, descuentos o bonificaciones') ,('3','G03 Gastos en general') ,('4','I01 Construcciones') ,('5','I02 Mobilario y equipo de oficina por inversiones') ,('6','I03 Equipo de transporte') ,('7','I04 Equipo de computo y accesorios') ,('8','I05 Dados, troqueles, moldes, matrices y herramental') ,('9','I06 Comunicaciones telefónicas') ,('10','I07 Comunicaciones satelitales') ,('11','I08 Otra maquinaria y equipo') ,('22','P01 Por definir')], string = "Uso CFDI",track_visibility='onchange',default='22')

    diasCredito = fields.Integer(string="Días de crédito",track_visibility='onchange')
    limbo  = fields.Boolean(string="Limbo", default=False)
    activo = fields.Boolean(string="Activo", default=False)
    #Dirección Fiscal
    
    direccion     = fields.Text(string="Dirección",track_visibility='onchange')

    estado       = fields.Selection([('Aguascalientes','Aguascalientes') ,('Baja California','Baja California') ,('Baja California Sur','Baja California Sur') ,('Campeche','Campeche') ,('Ciudad de México','Ciudad de México') ,('Coahuila','Coahuila') ,('Colima','Colima') ,('Chiapas','Chiapas') ,('Chihuahua','Chihuahua') ,('Durango','Durango') ,('Estado de México','Estado de México') ,('Guanajuato','Guanajuato') ,('Guerrero','Guerrero') ,('Hidalgo','Hidalgo') ,('Jalisco','Jalisco') ,('Michoacán','Michoacán') ,('Morelos','Morelos') ,('Nayarit','Nayarit') ,('Nuevo León','Nuevo León') ,('Oaxaca','Oaxaca') ,('Puebla','Puebla') ,('Querétaro','Querétaro') ,('Quintana Roo','Quintana Roo') ,('San Luis Potosí','San Luis Potosí') ,('Sinaloa','Sinaloa') ,('Sonora','Sonora') ,('Tabasco','Tabasco') ,('Tamaulipas','Tamaulipas') ,('Tlaxcala','Tlaxcala') ,('Veracruz','Veracruz') ,('Yucatán','Yucatán') ,('Zacatecas','Zacatecas')], string = "Estado",track_visibility='onchange')
    codPostal    = fields.Integer(string="C.P.",track_visibility='onchange')
    calle = fields.Text(string="Calle")
    exterior = fields.Text(string="No. exterior")
    interior = fields.Text(string="No. interior")
    colonia = fields.Text(string="Colonia")
    delegacion = fields.Text(string="Delegación")
    pago    = fields.Selection([("ANTICIPADO","Anticipado"),("VENCIDO","Vencido"),("MIXOT","Mixto")],string="Pago",track_visibility='onchange')
