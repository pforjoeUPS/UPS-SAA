# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 21:41:41 2021

@author: NVG9HXP
"""

import pandas as pd
from .import formats

def set_return_sheet(writer,df_returns,sheet_name='Daily Historical Returns'):
    """
    Create excel sheet for historical returns
    
    Parameters:
    writer -- excel writer
    df_returns -- dataframe
    sheet_name -- string
    """

    workbook = writer.book
    cell_format = formats.set_worksheet_format(workbook)
    df_empty = pd.DataFrame()
    df_empty.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1000, 21, cell_format)
    row = 0
    col = 0
    
    #percent format
    pct_fmt = formats.set_number_format(workbook,num_format='0.00%')
    #date format
    date_fmt = formats.set_number_format(workbook, num_format='mm/dd/yyyy')
        
    row_dim = row + df_returns.shape[0]
    col_dim = col + df_returns.shape[1]
    #    worksheet.write(row-1, 1, sheet_name, title_format)
    df_returns.to_excel(writer, sheet_name=sheet_name, startrow=row , startcol=col)   
    worksheet.conditional_format(row+1,col+1, row_dim, col_dim,{'type':'no_blanks',
                                  'format':pct_fmt})
    worksheet.conditional_format(row,col, row_dim, col,{'type':'no_blanks',
                                  'format':date_fmt})
    return 0

def set_corr_sheet(writer,corr_df,sheet_name='corr', color=False):
    """
    Create excel sheet for historical returns
    
    Parameters:
    writer -- excel writer
    df_returns -- dataframe
    sheet_name -- string
    """

    workbook = writer.book
    cell_format = formats.set_worksheet_format(workbook)
    df_empty = pd.DataFrame()
    df_empty.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1000, 21, cell_format)
    row = 0
    col = 0
    
    #digits format
    digits_fmt = formats.set_number_format(workbook,num_format='0.0000')
        
    row_dim = row + corr_df.shape[0]
    col_dim = col + corr_df.shape[1]
    
    corr_df.to_excel(writer, sheet_name=sheet_name, startrow=row , startcol=col)   
    worksheet.conditional_format(row+1,col+1, row_dim, col_dim,{'type':'duplicate',
                                  'format':digits_fmt})
    if color:
        worksheet.conditional_format(row,col, row_dim, col,{'type':'3_color_scale'})
    return 0

def set_ret_vol_sheet(writer,ret_vol_df,sheet_name='ret_vol'):
    """
    Create excel sheet for historical returns
    
    Parameters:
    writer -- excel writer
    df_returns -- dataframe
    sheet_name -- string
    """

    workbook = writer.book
    cell_format = formats.set_worksheet_format(workbook)
    df_empty = pd.DataFrame()
    df_empty.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1000, 21, cell_format)
    row = 0
    col = 0
    
    #percent format
    pct_fmt = formats.set_number_format(workbook,num_format='0.00%')
        
    row_dim = row + ret_vol_df.shape[0]
    col_dim = col + ret_vol_df.shape[1]
    
    ret_vol_df.to_excel(writer, sheet_name=sheet_name, startrow=row , startcol=col)   
    worksheet.conditional_format(row+1,col+1, row_dim, col_dim,{'type':'no_blanks',
                                  'format':pct_fmt})
    return 0

def set_wgts_sheet(writer,wgts_df,sheet_name='weights'):
    """
    Create excel sheet for historical returns
    
    Parameters:
    writer -- excel writer
    df_returns -- dataframe
    sheet_name -- string
    """

    workbook = writer.book
    cell_format = formats.set_worksheet_format(workbook)
    df_empty = pd.DataFrame()
    df_empty.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1000, 21, cell_format)
    row = 0
    col = 0
    
    #percent format
    pct_fmt = formats.set_number_format(workbook,num_format='0.00%')
    
    #digits format
    digits_fmt = formats.set_number_format(workbook,num_format='0.00')
        
    row_dim = row + wgts_df.shape[0]
    col_dim = col + wgts_df.shape[1]
    
    wgts_df.to_excel(writer, sheet_name=sheet_name, startrow=row , startcol=col)   
    worksheet.conditional_format(row+1,col+1, row_dim, col+1,{'type':'no_blanks',
                                  'format':pct_fmt})
    worksheet.conditional_format(row+1,col+2, row_dim, col+2,{'type':'no_blanks',
                                  'format':digits_fmt})
    worksheet.conditional_format(row+1,col+3, row_dim, col_dim,{'type':'no_blanks',
                                  'format':pct_fmt})
    return 0

def set_ef_port_sheet(writer,ports_df,sheet_name='weights'):
    """
    Create excel sheet for historical returns
    
    Parameters:
    writer -- excel writer
    df_returns -- dataframe
    sheet_name -- string
    """

    workbook = writer.book
    cell_format = formats.set_worksheet_format(workbook)
    df_empty = pd.DataFrame()
    df_empty.to_excel(writer, sheet_name=sheet_name, startrow=0, startcol=0)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1000, 21, cell_format)
    row = 0
    col = 0
    
    #percent format
    ret_vol_fmt = formats.set_number_format(workbook,num_format='0.00%')
    wgts_fmt = formats.set_number_format(workbook,num_format='0.00%')
    
    #digits format
    digits_fmt = formats.set_number_format(workbook,num_format='0.0000')
        
    row_dim = row + ports_df.shape[0]
    col_dim = col + ports_df.shape[1]
    
    ports_df.to_excel(writer, sheet_name=sheet_name, startrow=row , startcol=col)   
    worksheet.conditional_format(row+1,col+1, row_dim, col+2,{'type':'no_blanks',
                                  'format':ret_vol_fmt})
    worksheet.conditional_format(row+1,col+3, row_dim, col+3,{'type':'no_blanks',
                                  'format':digits_fmt})
    worksheet.conditional_format(row+1,col+4, row_dim, col_dim,{'type':'no_blanks',
                                  'format':wgts_fmt})
    return 0