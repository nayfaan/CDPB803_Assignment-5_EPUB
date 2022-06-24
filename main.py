import os, shutil, re

def add_line_to_ms(ms, line):
    ms.append(line)
    return ""

def clear_output():
    folder = "./output"
    file_path = ""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            if file_path:
                print('Deleted %s.' % (file_path))
        except Exception as e:
            print('ERROR: Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    #xhtml settings
    book_title = "Science in the Kitchen"
    css_href = "CSS/main.css"
    xhtml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
<title>'''+ book_title +'''</title>
<link rel="stylesheet" type="text/css" href="'''+ css_href +'''"/>
<meta charset="UTF-8" />
</head>
<body>
'''
    xhtml_footer = '''</body>
</html>'''
    
    #reading source ms
    with open('./input/to_be_proccessed.txt', newline='') as f:
        raw = f.read().splitlines()
    
    #groups paragraphs and tables
    ms = []
    temp_line = ""
    is_table = False
    
    for line in raw:
        if line:
            if line.strip() == "{{TABLE}}":
                if temp_line:
                    temp_line = add_line_to_ms(ms, temp_line)
                is_table = True
                temp_line = []
                
            if temp_line and not is_table:
                temp_line += " "
                
            if is_table:
                if not (line.strip() == "{{TABLE}}" or line.strip() == "{{/TABLE}}"):
                    temp_line.append(line)
            else:
                temp_line += line
                
            if line.strip() == "{{/TABLE}}":
                is_table = False
                temp_line = add_line_to_ms(ms, temp_line)
                
            if line.strip() == "{{NEWCHAP}}":
                temp_line = add_line_to_ms(ms, temp_line)
        else:
            if not is_table and temp_line:
                temp_line = add_line_to_ms(ms, temp_line)
    if temp_line:
        temp_line = add_line_to_ms(ms, temp_line)
        
    #adds italics tags
    for index, line in enumerate(ms):
        if type(line) is list:
            for index, tr in enumerate(line):
                line[index] = re.sub(r"_(.*?)_", r"<i>\1</i>", line[index])
        else:
            ms[index] = re.sub(r"_(.*?)_", r"<i>\1</i>", ms[index])
    
    #separates chapters
    ms_chapters = [[]]
    current_chapter = 0
    for para in ms:
        if type(para) is str:
            if para.strip() == "{{NEWCHAP}}":
                ms_chapters.append([])
                current_chapter += 1
            else:
                ms_chapters[current_chapter].append(para)
        else:
            ms_chapters[current_chapter].append(para)
            
    #outputs chapter files
    clear_output()
    for index, chapter in enumerate(ms_chapters):
        with open('output/chapter_'+ str(index).zfill(2) +'.xhtml', 'w') as f:
            f.write(xhtml_header)
            for para in chapter:
                if type(para) is str:
                    f.write("<p>"+ para +"</p>\n")
                else:
                    f.write("<table>\n")
                    for tr in para:
                        f.write("<tr><td>" + tr + "</td></tr>\n") 
                    f.write("</table>\n")
            f.write(xhtml_footer)
            f.close()
