import sys
import os
debug = False

# formats specified headers and results into visual table 
def formatToTable(headers, results):

    column_widths = [0]*len(headers)
    temp_results = results.copy()
    temp_results.append(tuple(headers))
    total_width = 0

    for row in temp_results:
        for index, item in enumerate(row):
            item = '' if item is None else str(item)
            if len(str(item)) > column_widths[index]:
                column_widths[index] = len(str(item))
            
    for value in column_widths:
        total_width += value

    border = '+-'
    for index, header in enumerate(headers):
        border += ('-'*column_widths[index]) + '-+-'
    print(border)

    title = '| '
    for index, header in enumerate(headers):
        title += f'{header:<{column_widths[index]}} | '
    print(title)
    print(border)
    
    for row in results:
        row_string = '| '
        for index, item in enumerate(row):
            item = '' if item is None else str(item)
            row_string += f'{item:<{column_widths[index]}} | '
        print(row_string)

    print(border)
    return

#Clears the terminal
def clearTerm():
    if not debug:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

#Checks to see if a string can be converted to integer
def isInputInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False