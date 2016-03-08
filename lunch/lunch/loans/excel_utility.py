# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import io as StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min
from .models import Loan, Device
from datetime import datetime

# solve:UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1: ordinal not in range(128).
#reload(sys)  
#sys.setdefaultencoding('utf8')

def WriteToExcel(request_data):
    #output = StringIO.StringIO()
    output = StringIO.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Summary")

    # excel styles
    title = workbook.add_format({
        #'bold': True,
        #'font_size': 14,
        #'align': 'center',
        #'valign': 'vcenter',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    # get data from db
    all_header = [
        'function_team', 'cocodri', 'pegadri', 'purpose', 'disassemble',
        'created_at', 'station', 'config', 'unit_no',
        'isn', 'failure_symptoms', 'utk', 'is_approved',
        'status'
    ]
    request_header = [
        'function_team', 'cocodri', 'pegadri', 'purpose', 'disassemble',
        'created_at'
    ]
    device_header = [
        'station', 'config', 'unit_no',
        'isn', 'failure_symptoms', 'utk', 'is_approved',
        'status'
    ]
    
    # write header
    worksheet_s.write(0, 0, ugettext("Date"), header)
    worksheet_s.write(0, 1, ugettext("Time"), header)
    worksheet_s.write(0, 2, ugettext("Function Team"), header)
    worksheet_s.write(0, 3, ugettext("Station"), header)
    worksheet_s.write(0, 4, ugettext("Config"), header)
    worksheet_s.write(0, 5, ugettext("Unit #"), header)
    worksheet_s.write(0, 6, ugettext("SN"), header)
    worksheet_s.write(0, 7, ugettext("Failure Symptoms"), header)
    worksheet_s.write(0, 8, ugettext("Disassemble"), header)
    worksheet_s.write(0, 9, ugettext("Purpose"), header)
    worksheet_s.write(0, 10, ugettext("CocoDRI"), header)
    worksheet_s.write(0, 11, ugettext("PegaDRI"), header)
    worksheet_s.write(0, 12, ugettext("Status"), header)
    worksheet_s.write(0, 13, ugettext("Approved"), header)

    # write data
    row = 1
    for idx, data in enumerate(request_data):
        device_data = Device.objects.filter(request_id=data.id)
        merge_start = row
        for jdx, cdata in enumerate(device_data):
            worksheet_s.write_string(row, 0, str(datetime.strftime(data.created_at,
                                    '%Y-%m-%d')), cell_center)
            worksheet_s.write_string(row, 1, str(datetime.strftime(data.created_at,
                                    '%H:%M:%S')), cell_center)
            worksheet_s.write_string(row, 2, str(data.function_team), cell_center)
            worksheet_s.write_string(row, 3, str(cdata.station), cell_center)
            worksheet_s.write_string(row, 4, str(cdata.config), cell_center)
            worksheet_s.write_string(row, 5, str(cdata.unit_no), cell_center)
            worksheet_s.write_string(row, 6, str(cdata.isn), cell_center)
            worksheet_s.write_string(row, 7, str(cdata.failure_symptoms), cell_center)
            worksheet_s.write_string(row, 8, str(data.disassemble), cell_center)
            worksheet_s.write_string(row, 9, str(data.purpose), cell_center)
            worksheet_s.write_string(row, 10, str(data.cocodri), cell_center)
            worksheet_s.write_string(row, 11, str(data.pegadri), cell_center)
            worksheet_s.write_string(row, 12, str(cdata.status), cell_center)
            worksheet_s.write_string(row, 13, str(cdata.is_approved), cell_center)
            row = row + 1
        # Merge cell
        if jdx != 0:
            worksheet_s.merge_range(merge_start, 9, row-1, 9, data.purpose, title)
            #worksheet_s.merge_range(merge_start, 1, row-1, 1, data.quantity, title)

    # change column widths
    description_col_width = 10
    worksheet_s.set_column('A:A', len('Date')+10)  # 
    worksheet_s.set_column('B:B', len("Time")+10)  #
    worksheet_s.set_column('C:C', len("Function Team"))  #
    worksheet_s.set_column('D:D', len("Station")+5)  #
    worksheet_s.set_column('E:E', len("Config")+5)  #
    worksheet_s.set_column('F:F', len("Unit #")+5)  #  
    worksheet_s.set_column('G:G', len("SN")+15)  # 
    worksheet_s.set_column('H:H', len("Failure Symptoms")+40)  # 
    worksheet_s.set_column('I:I', len("Disassemble"))  # 
    worksheet_s.set_column('J:J', len("Purpose")+25)  #
    worksheet_s.set_column('K:K', len("CocoDRI")+35)  #
    worksheet_s.set_column('L:L', len("PegaDRI")+35)  #
    worksheet_s.set_column('M:M', len("Status"))  #
    worksheet_s.set_column('N:N', len("Approved"))  #

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data
