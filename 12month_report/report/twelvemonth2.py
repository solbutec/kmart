# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from io import StringIO
import io
import json
import time
import xlsxwriter
import pytz
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class TwelveMonthReport(models.AbstractModel):
    _name = 'report.12month_report.twelve_month_xlsx_report'

    @api.model
    def get_report_values(self, docids, data=None):
        self.product_qty = 0.0
        self.total_inventory = []
        return {
                'doc_ids': self._ids,
                'docs': self,
                'data': data,
                'time': time,
                }

    def convert_withtimezone(self, userdate):
        """ 
        Convert to Time-Zone with compare to UTC
        """
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATETIME_FORMAT)
        tz_name = self.env.context.get('tz') or self.env.user.tz
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            # not need if you give default datetime into entry ;)
            user_datetime = user_date  # + relativedelta(hours=24.0)
            local_timestamp = context_tz.localize(user_datetime, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def _get_24quantity_value(self, date, locations , filter_product_ids=[]):
        vals = []
        added_date =  month = year = None
        added_date = date
        added_date = datetime.strptime(added_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=12)
        mon1 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=1)
        mon2 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=2)
        mon3 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=3)
        mon4 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=4)
        mon5 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=5)
        mon6 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=6)
        mon7= datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=7)
        mon8 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=8)
        mon9= datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=9)
        mon10 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=10)
        mon11 = datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - relativedelta(months=11)
        if len(str(added_date.month))==2:
            month = added_date.month
        else:
            month = '0'+str(added_date.month)
        year = str(added_date.year)
        if len(str(mon1.month))==2:
            month1 = mon1.month
        else:
            month1 = '0'+str(mon1.month)
        year1 = mon1.year
        if len(str(mon2.month))==2:
            month2 = mon2.month
        else:
            month2 = '0'+str(mon2.month)
        year2 = mon2.year
        if len(str(mon3.month))==2:
            month3 = mon3.month
        else:
            month3 = '0'+str(mon3.month)
        year3 = mon3.year
        if len(str(mon4.month))==2:
            month4 = mon4.month
        else:
            month4= '0'+str(mon4.month)
        year4= mon4.year
        if len(str(mon5.month))==2:
            month5 = mon5.month
        else:
            month5= '0'+str(mon5.month)
        year5= mon5.year
        if len(str(mon6.month))==2:
            month6 = mon6.month
        else:
            month6= '0'+str(mon6.month)
        year6= mon6.year
        if len(str(mon7.month))==2:
            month7 = mon7.month
        else:
            month7= '0'+str(mon7.month)
        year7= mon7.year
        if len(str(mon8.month))==2:
            month8 = mon8.month
        else:
            month8= '0'+str(mon8.month)
        year8= mon8.year
        if len(str(mon9.month))==2:
            month9= mon9.month
        else:
            month9= '0'+str(mon9.month)
        year9= mon9.year
        if len(str(mon10.month))==2:
            month10= mon10.month
        else:
            month10= '0'+str(mon10.month)
        year10= mon10.year
        if len(str(mon11.month))==2:
            month11= mon11.month
        else:
            month11= '0'+str(mon11.month)
        year11= mon11.year

# POS
        if len(str(added_date.month))==2:
            month = added_date.month
        else:
            month = '0'+str(added_date.month)
        year = str(added_date.year)
        if len(str(mon1.month))==2:
            month12 = mon1.month
        else:
            month12 = '0'+str(mon1.month)
        year12 = mon1.year
        if len(str(mon2.month))==2:
            month13 = mon2.month
        else:
            month13 = '0'+str(mon2.month)
        year13 = mon2.year
        if len(str(mon3.month))==2:
            month14 = mon3.month
        else:
            month14 = '0'+str(mon3.month)
        year14 = mon3.year
        if len(str(mon4.month))==2:
            month15 = mon4.month
        else:
            month15= '0'+str(mon4.month)
        year15= mon4.year
        if len(str(mon5.month))==2:
            month16 = mon5.month
        else:
            month16= '0'+str(mon5.month)
        year16= mon5.year
        if len(str(mon6.month))==2:
            month17 = mon6.month
        else:
            month17= '0'+str(mon6.month)
        year17= mon6.year
        if len(str(mon7.month))==2:
            month18 = mon7.month
        else:
            month18= '0'+str(mon7.month)
        year18= mon7.year
        if len(str(mon8.month))==2:
            month19 = mon8.month
        else:
            month19= '0'+str(mon8.month)
        year19= mon8.year
        if len(str(mon9.month))==2:
            month20= mon9.month
        else:
            month20= '0'+str(mon9.month)
        year20= mon9.year
        if len(str(mon10.month))==2:
            month21= mon10.month
        else:
            month21= '0'+str(mon10.month)
        year21= mon10.year
        if len(str(mon11.month))==2:
            month22= mon11.month
        else:
            month22= '0'+str(mon11.month)
        year22= mon11.year

# Ecommerces
        if len(str(added_date.month)) == 2:
            month = added_date.month
        else:
            month = '0' + str(added_date.month)
        year = str(added_date.year)
        if len(str(mon1.month)) == 2:
            month23 = mon1.month
        else:
            month23 = '0' + str(mon1.month)
        year23 = mon1.year
        if len(str(mon2.month)) == 2:
            month24 = mon2.month
        else:
            month24 = '0' + str(mon2.month)
        year24 = mon2.year
        if len(str(mon3.month)) == 2:
            month25 = mon3.month
        else:
            month25 = '0' + str(mon3.month)
        year25 = mon3.year
        if len(str(mon4.month)) == 2:
            month26 = mon4.month
        else:
            month26 = '0' + str(mon4.month)
        year26 = mon4.year
        if len(str(mon5.month)) == 2:
            month27 = mon5.month
        else:
            month27 = '0' + str(mon5.month)
        year27 = mon5.year
        if len(str(mon6.month)) == 2:
            month28 = mon6.month
        else:
            month28 = '0' + str(mon6.month)
        year28 = mon6.year
        if len(str(mon7.month)) == 2:
            month29 = mon7.month
        else:
            month29 = '0' + str(mon7.month)
        year29 = mon7.year
        if len(str(mon8.month)) == 2:
            month30 = mon8.month
        else:
            month30 = '0' + str(mon8.month)
        year30 = mon8.year
        if len(str(mon9.month)) == 2:
            month31 = mon9.month
        else:
            month31 = '0' + str(mon9.month)
        year31 = mon9.year
        if len(str(mon10.month)) == 2:
            month32 = mon10.month
        else:
            month32 = '0' + str(mon10.month)
        year32 = mon10.year
        if len(str(mon11.month)) == 2:
            month33 = mon11.month
        else:
            month33 = '0' + str(mon11.month)
        year33 = mon11.year

        if not filter_product_ids:
            raise UserError(_('Product Line does not exit please select product.'))
        print("location",locations)
        self._cr.execute('''SELECT pt.name,pc.name as categ,pc.parent_id as parent,pt.list_price as list_price, pp.id,
        pp.default_code,par.name as supplier,pt.name as product, pb.name as brand, pm.name as make, ps.name as seasonal,
        pk.name as packing,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) qty1,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty2,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty3,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty4,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty5,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty6,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty7,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty8,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty9,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty10,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty11,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN sale_order s ON (s.id=p.sale_id) 
                WHERE p.sale_id is not null AND p.website_id is null AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty12,
                
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) qty13,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty14,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty15,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty16,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty17,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty18,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty19,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty20,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty21,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty22,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id) 
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty23,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN stock_picking_type t ON (t.id=p.picking_type_id)
                WHERE t.name='PoS Orders' AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty24,
                
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) qty25,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty26,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty27,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty28,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty29,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty30,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty31,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty32,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty33,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty34,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty35,
            (select sum(sm.product_qty) FROM stock_move sm LEFT JOIN stock_location l ON (sm.location_id=l.id)    
                LEFT JOIN stock_picking p ON (sm.picking_id=p.id) LEFT JOIN website w ON (w.id=p.website_id) 
                WHERE p.website_id=w.id AND date_part('month',sm.date)= %s AND date_part('year',sm.date)= %s 
                AND sm.product_id = pp.id AND sm.date > %s AND sm.location_id in %s) as qty36,
                
            /*CASE WHEN pt.uom_id = m.product_uom 
            THEN pu.name 
            ELSE (select name from uom_uom where id = pt.uom_id) end AS uom*/
            pu.name AS uom,pp.barcode as barcode
            FROM product_product pp
                LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                LEFT JOIN uom_uom pu ON (pt.uom_id=pu.id)
                LEFT JOIN product_brand pb ON (pb.id = pt.product_brand_id)
                LEFT JOIN product_make pm ON (pm.id = pt.product_make_id)
                LEFT JOIN product_seasonal ps ON (ps.id = pt.product_seasonal_id)
                LEFT JOIN product_packing pk ON (pk.id = pt.product_packing_id)
                LEFT JOIN res_partner par ON (par.id = pt.supplier_id)
                LEFT JOIN product_category pc ON (pc.id = pt.categ_id)
                WHERE pp.active=True
                AND pp.id in %s
                GROUP BY pp.id,pt.name,pc.name ,pc.parent_id ,pt.list_price,
                pp.id,pp.default_code,par.name,pt.name , pb.name, pm.name, ps.name, pk.name,
                pt.uom_id,pu.name,pp.barcode
                 ''',(month,year,end_date,tuple(locations),month1,year1,end_date,tuple(locations),month2,year2,end_date,tuple(locations),
                      month3,year3,end_date,tuple(locations),month4,year4,end_date,tuple(locations),month5,year5,end_date,tuple(locations),
                      month6,year6,end_date,tuple(locations),month7,year7,end_date,tuple(locations),month8,year8,end_date,tuple(locations),
                      month9,year9,end_date,tuple(locations),month10,year10,end_date,tuple(locations),month11,year11,end_date,tuple(locations),
                      month,year,end_date,tuple(locations),month12,year12,end_date,tuple(locations),month13,year13,end_date,tuple(locations),
                      month14,year14,end_date,tuple(locations),month15,year15,end_date,tuple(locations),month16,year16,end_date,tuple(locations),
                      month17,year17,end_date,tuple(locations),month18,year18,end_date,tuple(locations),month19,year19,end_date,tuple(locations),
                      month20,year20,end_date,tuple(locations),month21,year21,end_date,tuple(locations),month22,year22,end_date,tuple(locations),
                      month,year,end_date,tuple(locations),month23,year23,end_date,tuple(locations),month24,year24,end_date,tuple(locations),
                      month25,year25,end_date,tuple(locations),month26,year26,end_date,tuple(locations),month27,year27,end_date,tuple(locations),
                      month28,year28,end_date,tuple(locations),month29,year29,end_date,tuple(locations),month30,year30,end_date,tuple(locations),
                      month31,year31,end_date,tuple(locations),month32,year32,end_date,tuple(locations),month33,year33,end_date,tuple(locations),
                      tuple(filter_product_ids)))
        values = self._cr.dictfetchall()
        vals.append(values)
        return vals

    def get_report_name(self):
        return _('Twelve Month Report By Warehouse')

    def get_report_filename(self, options):
        return self.get_report_name().lower().replace(' ', '_')
        
    def find_warehouses(self,company_id):
        """
        Find all warehouses
        """
        return [x.id for x in self.env['stock.warehouse'].search([('company_id','=',company_id)])]

    def _find_locations(self, warehouse):
        """
        Find warehouse stock locations and its childs.
            -All stock reports depends on stock location of warehouse.
        """
        warehouse_obj = self.env['stock.warehouse']
        location_obj = self.env['stock.location']
        store_location_id = warehouse_obj.browse(warehouse).view_location_id.id
        return [x.id for x in location_obj.search([('location_id', 'child_of', store_location_id)])]

    def _compare_with_company(self, warehouse, company):
        """
        Company loop check ,whether it is in company of not.
        """
        company_id = self.env['stock.warehouse'].browse(warehouse).read(['company_id'])[0]['company_id']
        if company_id[0] != company:
            return False
        return True

    def _get_lines(self, data, company):
        """
        Process:
            Pass start date, end date, locations to get data from moves,
            Merge those data with locations,
        Return:
            {location : [{},{},{}...], location : [{},{},{}...],...}
        """
        date = self.convert_withtimezone(data['form']['date']+' 00:00:00')
        warehouse_ids = data['form'] and data['form'].get('warehouse_ids',[]) or []
        filter_product_ids = data['form'] and data['form'].get('filter_product_ids') or []
        location_id = data['form'] and data['form'].get('location_id') or False
        if not warehouse_ids:
            warehouse_ids = self.find_warehouses(company)
        final_values = {}
        for warehouse in warehouse_ids:
            #looping for only warehouses which is under current company
            if self._compare_with_company(warehouse, company[0]):
                locations = self._find_locations(warehouse)
                if location_id:
                    if (location_id in locations):
                        final_values.update({
                                    warehouse:self._get_24quantity_value(date, [location_id],filter_product_ids)
                                    })

                else:
                    final_values.update({
                                    warehouse:self._get_24quantity_value(date, locations,filter_product_ids)
                                    })
        self.value_exist = final_values
        return final_values

    def xlsx_export(self,datas):
        return {
                    'type': 'ir_actions_account_report_download',
                    'data': {'model': 'report.12month_report.twelve_month_xlsx_report',
                    'options': json.dumps(datas, indent=4, sort_keys=True, default=str),
                    'output_format': 'xlsx',
                    'financial_id': self.env.context.get('id'),
                    }
                }

    @api.multi
    def get_xlsx(self, options,response):
        output = io.BytesIO()
        get_lines=[]
        date = None
        location_name = None
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(self.get_report_name())
        fromat0 = workbook.add_format({ 'bold': True,'align': 'center','font_size': 14,})
        fromat1 = workbook.add_format({ 'align': 'center', 'bold': True, 'border': True,})
        fromat2 = workbook.add_format({ 'align': 'center','border': True})
        fromat3 = workbook.add_format({ 'align': 'left', 'border': True})
        fromat4 = workbook.add_format({ 'align': 'right', 'border': True})
        fromat5 = workbook.add_format({'align': 'center', 'border': True})
        sheet.set_column(0, 0, 15) #  Set the first column width to 15
        company_name = warehouse_name =warehouse_name_group =''
        location_id = options['form'] and options['form'].get('location_id') or False
        if location_id:
            print ("Location", location_id)
            location_name = self.env['stock.location'].search([('id', '=', location_id)]).name
        date = datetime.today().strftime('%Y-%m-%d')
        cid=options['form']['company_id']
        if cid:
            for company in self.env['res.company'].browse(cid).name_get():
                company_name += str(company[1]) + ','
            company_name = company_name[:-1]
        else:
            company_name = 'All'
        warehouse_id = options['form']['warehouse_ids']
        if warehouse_id:
            for warehouse in self.env['stock.warehouse'].browse(warehouse_id).name_get():
                warehouse_name += (warehouse[1] + ',')
            warehouse_name = warehouse_name[:-1]
        else:
            warehouse_name = 'All'
        y_offset = 0
        sheet.merge_range(y_offset, 7, y_offset, 10, _('Twelve Month Report'),fromat0)
        y_offset +=2
        sheet.write(y_offset, 0, _('Warehouse Name'),fromat1)
        sheet.write(y_offset, 1, warehouse_name,fromat2)
        y_offset +=1
        sheet.write(y_offset, 0, _('Location Name'),fromat1)
        sheet.write(y_offset, 1, location_name,fromat2)
        y_offset +=1
        sheet.write(y_offset, 0, _('Date'),fromat1)
        sheet.write(y_offset, 1, date,fromat2)
        y_offset +=2
        sheet.merge_range(y_offset, 0, y_offset + 1, 0,  _('Item Code'),fromat1)
        sheet.merge_range(y_offset, 1, y_offset + 1, 1, _('Barcode'),fromat1)
        sheet.merge_range(y_offset, 2, y_offset + 1, 2, _('Multi-Barcode'),fromat1)
        sheet.merge_range(y_offset, 3, y_offset + 1, 3, _('Product Name'),fromat1)
        sheet.merge_range(y_offset, 4, y_offset + 1, 4, _('UOM'),fromat1)
        sheet.merge_range(y_offset, 5, y_offset + 1, 5, _('Made In'), fromat1)
        sheet.merge_range(y_offset, 6, y_offset + 1, 6, _('Promotion'), fromat1)
        sheet.merge_range(y_offset, 7, y_offset + 1, 7, _('Cut Item'), fromat1)
        sheet.merge_range(y_offset, 8, y_offset + 1, 8, _('Remark'), fromat1)
        sheet.merge_range(y_offset, 9, y_offset + 1, 9, _('Internal Notes'), fromat1)
        sheet.merge_range(y_offset, 10, y_offset + 1, 10, _('Brand Name'),fromat1)
        sheet.merge_range(y_offset, 11, y_offset + 1, 11, _('Parent Category'),fromat1)
        sheet.merge_range(y_offset, 12, y_offset + 1, 12, _('Child Category'),fromat1)
        sheet.merge_range(y_offset, 13, y_offset + 1, 13, _('Supplier Name'),fromat1)
        sheet.merge_range(y_offset, 14, y_offset + 1, 14, _('Supplier Price'), fromat1)
        sheet.merge_range(y_offset, 15, y_offset + 1, 15, _('Sales Price'),fromat1)
        sheet.merge_range(y_offset, 16, y_offset + 1, 16, _('Cost Price'),fromat1)


        month_date = options['form']['date']+' 00:00:00'
        month_date = datetime.strptime(month_date, '%Y-%m-%d %H:%M:%S')
        mon1 = month_date - relativedelta(months=1)
        mon2 = month_date - relativedelta(months=2)
        mon3 = month_date - relativedelta(months=3)
        mon4 = month_date - relativedelta(months=4)
        mon5 = month_date - relativedelta(months=5)
        mon6 = month_date - relativedelta(months=6)
        mon7 = month_date - relativedelta(months=7)
        mon8 = month_date - relativedelta(months=8)
        mon9 = month_date - relativedelta(months=9)
        mon10 = month_date - relativedelta(months=10)
        mon11 = month_date - relativedelta(months=11)


        sheet.merge_range(y_offset, 17, y_offset, 20, _(mon11.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 21, y_offset, 24, _(mon10.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 25, y_offset, 28, _(mon9.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 29, y_offset, 32, _(mon8.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 33, y_offset, 36, _(mon7.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 37, y_offset, 40, _(mon6.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 41, y_offset, 44, _(mon5.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 45, y_offset, 48, _(mon4.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 49, y_offset, 52, _(mon3.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 53, y_offset, 56, _(mon2.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 57, y_offset, 60, _(mon1.strftime("%b-%y")),fromat5)
        sheet.merge_range(y_offset, 61, y_offset, 64, _(month_date.strftime("%b-%y")),fromat5)

        sheet.merge_range(y_offset, 65, y_offset, 67, _('Average'),fromat5)

        sheet.merge_range(y_offset, 68, y_offset + 1, 68, _('On Hand'),fromat1)
        sheet.merge_range(y_offset, 69, y_offset + 1, 69, _('Forecasted'), fromat1)
        y_offset +=1

        sheet.write(y_offset, 17, _('POS'), fromat1)
        sheet.write(y_offset, 18, _('Wholesales'), fromat1)
        sheet.write(y_offset, 19, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 20, _('Total'), fromat1)
        sheet.write(y_offset, 21, _('POS'), fromat1)
        sheet.write(y_offset, 22, _('Wholesales'), fromat1)
        sheet.write(y_offset, 23, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 24, _('Total'), fromat1)
        sheet.write(y_offset, 25, _('POS'), fromat1)
        sheet.write(y_offset, 26, _('Wholesales'), fromat1)
        sheet.write(y_offset, 27, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 28, _('Total'), fromat1)
        sheet.write(y_offset, 29, _('POS'), fromat1)
        sheet.write(y_offset, 30, _('Wholesales'), fromat1)
        sheet.write(y_offset, 31, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 32, _('Total'), fromat1)
        sheet.write(y_offset, 33, _('POS'), fromat1)
        sheet.write(y_offset, 34, _('Wholesales'), fromat1)
        sheet.write(y_offset, 35, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 36, _('Total'), fromat1)
        sheet.write(y_offset, 37, _('POS'), fromat1)
        sheet.write(y_offset, 38, _('Wholesales'), fromat1)
        sheet.write(y_offset, 39, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 40, _('Total'), fromat1)
        sheet.write(y_offset, 41, _('POS'), fromat1)
        sheet.write(y_offset, 42, _('Wholesales'), fromat1)
        sheet.write(y_offset, 43, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 44, _('Total'), fromat1)
        sheet.write(y_offset, 45, _('POS'), fromat1)
        sheet.write(y_offset, 46, _('Wholesales'), fromat1)
        sheet.write(y_offset, 47, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 48, _('Total'), fromat1)
        sheet.write(y_offset, 49, _('POS'), fromat1)
        sheet.write(y_offset, 50, _('Wholesales'), fromat1)
        sheet.write(y_offset, 51, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 52, _('Total'), fromat1)
        sheet.write(y_offset, 53, _('POS'), fromat1)
        sheet.write(y_offset, 54, _('Wholesales'), fromat1)
        sheet.write(y_offset, 55, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 56, _('Total'), fromat1)
        sheet.write(y_offset, 57, _('POS'), fromat1)
        sheet.write(y_offset, 58, _('Wholesales'), fromat1)
        sheet.write(y_offset, 59, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 60, _('Total'), fromat1)
        sheet.write(y_offset, 61, _('POS'), fromat1)
        sheet.write(y_offset, 62, _('Wholesales'), fromat1)
        sheet.write(y_offset, 63, _('Ecommerce'), fromat1)
        sheet.write(y_offset, 64, _('Total'), fromat1)
        sheet.write(y_offset, 65, _('POS'), fromat1)
        sheet.write(y_offset, 66, _('Wholesales'), fromat1)
        sheet.write(y_offset, 67, _('Ecommerce'), fromat1)

        lines = self._get_lines(options, options['form']['company_id'])
        print ("lines ::::::::::::::::::::::::::",lines)
        y_offset += 1
        if lines:
            for l in lines:
                for loop in lines[l]:
                    cost_price = 0
                    for line in loop:
                        avg = 0
                        avg1 = 0
                        avg2 = 0
                        sum = 0
                        sum1 = 0
                        sum2 = 0
                        sum3 = 0
                        sum4 = 0
                        sum5 = 0
                        sum6 = 0
                        sum7 = 0
                        sum8 = 0
                        sum9 = 0
                        sum10 = 0
                        sum11 = 0
                        product_tmpl_id = self.env['product.template'].search([('default_code','=',line['default_code']),('name','=',line['product'])])
                        
                        print ("product_tmpl_id :::::::::;",product_tmpl_id.image_small)
                        remark = product_tmpl_id.product_remark
                        description = product_tmpl_id.description
                        price = product_tmpl_id.standard_price
                        supplier_price = product_tmpl_id.final_purchase_price
                        product_id = self.env['product.product'].search([('product_tmpl_id','=',product_tmpl_id.id)], limit=1)
                        multi_barcode = self.env['product.multi.barcode'].search([('product_tmpl_id','=',product_tmpl_id.id)], limit=1)
                        parent_categ_name = self.env['product.category'].search([('id','=',line['parent'])]).complete_name
                        sq_quantity_ids= self.env['stock.quant'].search([('product_id','=',product_id.id),('location_id','=',location_id)])

                        sq_quantity = 0.0
                        if sq_quantity_ids:
                            for s in sq_quantity_ids:
                                sq_quantity += s.quantity

                        force_quantity = product_tmpl_id.virtual_available
                        sheet.write(y_offset, 0, line['default_code'],fromat2)
                        sheet.write(y_offset, 1, line['barcode'],fromat2)
                        sheet.write(y_offset, 2, multi_barcode.barcode or '',fromat2)
                        sheet.write(y_offset, 3, line['product'],fromat3)
                        sheet.write(y_offset, 4, line['uom'],fromat2)
                        sheet.write(y_offset, 5, line['make'], fromat2)
                        sheet.write(y_offset, 6, line['seasonal'], fromat2)
                        sheet.write(y_offset, 7, line['packing'], fromat2)
                        sheet.write(y_offset, 8, remark, fromat2)
                        sheet.write(y_offset, 9, description, fromat2)
                        sheet.write(y_offset, 10, line['brand'],fromat2)
                        sheet.write(y_offset, 11, parent_categ_name,fromat2)
                        sheet.write(y_offset, 12, line['categ'],fromat2)
                        sheet.write(y_offset, 13, line['supplier'],fromat3)
                        sheet.write(y_offset, 14, supplier_price, fromat3)
                        sheet.write(y_offset, 15, line['list_price'],fromat2)
                        sheet.write(y_offset, 16, price,fromat2)

                        # POS ----
                        sheet.write(y_offset, 17, line['qty24'], fromat2)
                        if line['qty24'] != None:
                            avg += int(line['qty24'])
                            sum11 += int(line['qty24'])
                        sheet.write(y_offset, 21, line['qty23'], fromat2)
                        if line['qty23'] != None:
                            avg += int(line['qty23'])
                            sum10 += int(line['qty23'])
                        sheet.write(y_offset, 25, line['qty22'], fromat2)
                        if line['qty22'] != None:
                            avg += int(line['qty22'])
                            sum9 += int(line['qty22'])
                        sheet.write(y_offset, 29, line['qty21'], fromat2)
                        if line['qty21'] != None:
                            avg += int(line['qty21'])
                            sum8 += int(line['qty21'])
                        sheet.write(y_offset, 33, line['qty20'], fromat2)
                        if line['qty20'] != None:
                            avg += int(line['qty20'])
                            sum7 += int(line['qty20'])
                        sheet.write(y_offset, 37, line['qty19'], fromat2)
                        if line['qty19'] != None:
                            avg += int(line['qty19'])
                            sum6 += int(line['qty19'])
                        sheet.write(y_offset, 41, line['qty18'], fromat2)
                        if line['qty18'] != None:
                            avg += int(line['qty18'])
                            sum5 += int(line['qty18'])
                        sheet.write(y_offset, 45, line['qty17'], fromat2)
                        if line['qty17'] != None:
                            avg += int(line['qty17'])
                            sum4 += int(line['qty17'])
                        sheet.write(y_offset, 49, line['qty16'], fromat2)
                        if line['qty16'] != None:
                            avg += int(line['qty16'])
                            sum3 += int(line['qty16'])
                        sheet.write(y_offset, 53, line['qty15'], fromat2)
                        if line['qty15'] != None:
                            avg += int(line['qty15'])
                            sum2 += int(line['qty15'])
                        sheet.write(y_offset, 57, line['qty14'], fromat2)
                        if line['qty14'] != None:
                            avg += int(line['qty14'])
                            sum1 += int(line['qty14'])
                        sheet.write(y_offset, 61, line['qty13'], fromat2)
                        if line['qty13'] != None:
                            avg += int(line['qty13'])
                            sum += int(line['qty13'])

                            # Sales
                        sheet.write(y_offset, 18, line['qty12'], fromat2)
                        if line['qty12'] != None:
                            avg1 += int(line['qty12'])
                            sum11 += int(line['qty12'])
                        sheet.write(y_offset, 22, line['qty11'], fromat2)
                        if line['qty11'] != None:
                            avg1 += int(line['qty11'])
                            sum10 += int(line['qty11'])
                        sheet.write(y_offset, 26, line['qty10'], fromat2)
                        if line['qty10'] != None:
                            avg1 += int(line['qty10'])
                            sum9 += int(line['qty10'])
                        sheet.write(y_offset, 30, line['qty9'], fromat2)
                        if line['qty9'] != None:
                            avg1 += int(line['qty9'])
                            sum8 += int(line['qty9'])
                        sheet.write(y_offset, 34, line['qty8'], fromat2)
                        if line['qty8'] != None:
                            avg1 += int(line['qty8'])
                            sum7 += int(line['qty8'])
                        sheet.write(y_offset, 38, line['qty7'], fromat2)
                        if line['qty7'] != None:
                            avg1 += int(line['qty7'])
                            sum6 += int(line['qty7'])
                        sheet.write(y_offset, 42, line['qty6'], fromat2)
                        if line['qty6'] != None:
                            avg1 += int(line['qty6'])
                            sum5 += int(line['qty6'])
                        sheet.write(y_offset, 46, line['qty5'], fromat2)
                        if line['qty5'] != None:
                            avg1 += int(line['qty5'])
                            sum4 += int(line['qty5'])
                        sheet.write(y_offset, 50, line['qty4'], fromat2)
                        if line['qty4'] != None:
                            avg1 += int(line['qty4'])
                            sum3 += int(line['qty4'])
                        sheet.write(y_offset, 54, line['qty3'], fromat2)
                        if line['qty3'] != None:
                            avg1 += int(line['qty3'])
                            sum2 += int(line['qty3'])
                        sheet.write(y_offset, 58, line['qty2'], fromat2)
                        if line['qty2'] != None:
                            avg1 += int(line['qty2'])
                            sum1 += int(line['qty2'])
                        sheet.write(y_offset, 62, line['qty1'], fromat2)
                        if line['qty1'] != None:
                            avg1 += int(line['qty1'])
                            sum += int(line['qty1'])

                            # Ecommerces ---
                        sheet.write(y_offset, 19, line['qty36'], fromat2)
                        if line['qty36'] != None:
                            avg2 += int(line['qty36'])
                            sum11 += int(line['qty36'])
                        sheet.write(y_offset, 23, line['qty35'], fromat2)
                        if line['qty35'] != None:
                            avg2 += int(line['qty35'])
                            sum10 += int(line['qty35'])
                        sheet.write(y_offset, 27, line['qty34'], fromat2)
                        if line['qty34'] != None:
                            avg2 += int(line['qty34'])
                            sum9 += int(line['qty34'])
                        sheet.write(y_offset, 31, line['qty33'], fromat2)
                        if line['qty33'] != None:
                            avg2 += int(line['qty33'])
                            sum8 += int(line['qty33'])
                        sheet.write(y_offset, 35, line['qty32'], fromat2)
                        if line['qty32'] != None:
                            avg2 += int(line['qty32'])
                            sum7 += int(line['qty32'])
                        sheet.write(y_offset, 39, line['qty31'], fromat2)
                        if line['qty31'] != None:
                            avg2 += int(line['qty31'])
                            sum6 += int(line['qty31'])
                        sheet.write(y_offset, 43, line['qty30'], fromat2)
                        if line['qty30'] != None:
                            avg2 += int(line['qty30'])
                            sum5 += int(line['qty30'])
                        sheet.write(y_offset, 47, line['qty29'], fromat2)
                        if line['qty29'] != None:
                            avg2 += int(line['qty29'])
                            sum4 += int(line['qty29'])
                        sheet.write(y_offset, 51, line['qty28'], fromat2)
                        if line['qty28'] != None:
                            avg2 += int(line['qty28'])
                            sum3 += int(line['qty28'])
                        sheet.write(y_offset, 55, line['qty27'], fromat2)
                        if line['qty27'] != None:
                            avg2 += int(line['qty27'])
                            sum2 += int(line['qty27'])
                        sheet.write(y_offset, 59, line['qty26'], fromat2)
                        if line['qty26'] != None:
                            avg2 += int(line['qty26'])
                            sum1 += int(line['qty26'])
                        sheet.write(y_offset, 63, line['qty25'], fromat2)
                        if line['qty25'] != None:
                            avg2 += int(line['qty25'])
                            sum += int(line['qty25'])

                        sheet.write(y_offset, 20, sum11, fromat2)
                        sheet.write(y_offset, 24, sum10, fromat2)
                        sheet.write(y_offset, 28, sum9, fromat2)
                        sheet.write(y_offset, 32, sum8, fromat2)
                        sheet.write(y_offset, 36, sum7, fromat2)
                        sheet.write(y_offset, 40, sum6, fromat2)
                        sheet.write(y_offset, 44, sum5, fromat2)
                        sheet.write(y_offset, 48, sum4, fromat2)
                        sheet.write(y_offset, 52, sum3, fromat2)
                        sheet.write(y_offset, 56, sum2, fromat2)
                        sheet.write(y_offset, 60, sum1, fromat2)
                        sheet.write(y_offset, 64, sum, fromat2)

                        # avg
                        sheet.write(y_offset, 65, avg/12,fromat2)
                        sheet.write(y_offset, 66, avg1/12,fromat2)
                        sheet.write(y_offset, 67, avg2/12,fromat2)

                        sheet.write(y_offset, 68, sq_quantity,fromat2)
                        sheet.write(y_offset, 69, force_quantity, fromat2)
                        y_offset +=1
                        sum = 0
                        sum1 = 0
                        sum2 = 0
                        sum3 = 0
                        sum4 = 0
                        sum5 = 0
                        sum6 = 0
                        sum7 = 0
                        sum8 = 0
                        sum9 = 0
                        sum10 = 0
                        sum11 = 0
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()