import calendar
import time
import re

def remove_headers(chunk):
    index = chunk.find(b'\r\n\r\n')
    if index != -1:
        chunk = chunk[index + 4:]
    return chunk

def get_current_timestamp():
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    return time_stamp

def construct_name_of_file_part(filename, part_num):
    return filename + "_" + str(part_num)

def extract_file_format_from_headers(chunk):
    match = re.search(rb'filename="[^"]+\.(.*?)\"', chunk, re.S)

    if match:
        return str(match.group(1), 'UTF-8')
    else:
        return ""
    
def extract_filename_from_headers(chunk):
    match = re.search(rb'filename="(.+?)(\.[^.]*|$)"', chunk, re.S)

    if match:
        return str(match.group(1), 'UTF-8')
    else:
        return ""