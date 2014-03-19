#!/usr/bin/env python3
# Written by Michael Younkin in 2014. This work is in the public domain.

HELP_TEXT = '''
music_table.py
--------------

SYNOPSIS

    python music_table.py -h
    python music_table.py URL_PREFIX

DESCRIPTION

    This program generates HTML for the GSO website's "listen" page. It will
    accept text in CSV format from STDIN and writes the HTML table to STDOUT.
    You can copy and paste the output directly onto the GSO website's listen
    page.

SAMPLE INPUT

    Piece,Game,Performers,Arrangers,Filename
    Piece Name,Game Name,Michael,Younkin,my_piece
    Piece2,Game2,Younkin,Michael,my_second_piece

OPTIONS

    -h, --help  print this message

EXAMPLES

    All examples assume the bash shell. Commands will differ based on how piping
    works in your particular environment.

    cat 'music_data.csv' | python music_table.py "audio"> music_table.html

    Send the file 'music_data.csv' to music_table.py via STDIN, save the output
    of the script to 'music_table.html'. All URLs will be
    "audio/<piece name without spaces>.wav" or ".mp3" (no < >).
'''

TABLE_START = '''
<table>
<thead>
<tr><th>Piece</th><th>Game</th><th>Performers</th><th>Arrangers</th><th>Download</th></tr>
</thead>
<tbody>
'''

TABLE_END = '''
</tbody>
</table>
'''

ROW_TEMPLATE = '''
<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>
'''

DOWNLOAD_TEMPLATE = '''
<ul>
<li><a href="{0}">High Quality (.wav)</a></li>
<li><a href="{1}">Low Quality (.mp3)</a></li>
</ul>
'''

from sys import argv,exit,stdin,stderr
import csv

def main():
    if len(argv) != 2:
        print_error('invalid number of arguments')
        print_help()
        exit(1)
    if argv[1] == '-h' or argv[1] == '--help':
        print_help()
        exit(0)

    download_prefix = argv[1]

    music_data = csv.reader(stdin)
    next(music_data)
    print_table_start()
    for row in music_data:
        print_table_row(row, download_prefix)
    print_table_end()

def print_error(msg):
    print('Error: {0}\n'.format(msg))

def print_help():
    print(HELP_TEXT)

def print_table_start():
    print(TABLE_START)

def print_table_row(row, dirname):
    download_html = get_download_html(row, dirname)
    format_args = row[:-1]
    format_args.append(download_html)
    row_str = ROW_TEMPLATE.format(*format_args)
    print(row_str)

def print_table_end():
    print(TABLE_END)

def get_download_html(row, download_prefix):
    basename = row[4]
    filename = '{0}/{1}'.format(download_prefix, basename)
    high_url = filename + '.wav'
    low_url = filename + '.mp3'
    return DOWNLOAD_TEMPLATE.format(high_url, low_url)

main()
