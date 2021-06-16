import os
from dearpygui.core import *
from dearpygui.simple import *
from PyPDF2 import PdfFileReader, PdfFileWriter
from easygui import diropenbox, fileopenbox, filesavebox

#searches for pdf files in a folder and add them to the list
def findfiles(path, l=[]):
    for folder, subfs, files in os.walk(path):
        for file in files:
            f = file.split('.')
            if f[-1] == 'pdf':
                l.append({"name": f[0], "status": True, "path": folder + '/' + file})
                with open(l[-1]["path"], 'rb') as f:
                    pdf = PdfFileReader(f)
                    l[-1]["p"] = pdf.getNumPages()
        break
    return l

#adds a pdf file to the list
def addfile(path,file,l=[]):
        f = file.split('.')
        if f[-1] == 'pdf':
            l.append({"name": f[0], "status": True, "path": path})
            with open(l[-1]["path"], 'rb') as f:
                pdf = PdfFileReader(f)
                l[-1]["p"] = pdf.getNumPages()
        return l

#merge all selected items to 1 pdf
def merge(l, output):
    pdf_writer = PdfFileWriter()
    paths = []
    for i in range(len(l)):
        if l[i]["status"]:
            paths.append(l[i]["path"])
    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output, 'wb') as out:
        pdf_writer.write(out)

#change the order of a item in the list
def verplaats(l,i,ud):
    temp = l[i]
    del l[i]
    if ud == "u":
        l.insert(i-1,temp)
    else:
        l.insert(i+1,temp)
    return l

#shows the window for adding a file to the list
def add_file(sender,data):
    l = get_data('list')
    f = fileopenbox(title="Kies een file", default='*.pdf', filetypes="*.pdf", multiple=False)
    l = addfile(f,f.split('\\')[-1], l)
    add_data('list',l)
    del_files()
    display_files()
 
#shows the window for adding a folder to the list
def add_folder(sender,data):
    l = get_data('list')
    path = diropenbox(title="Kies een folder") 
    l = findfiles(path, l)
    add_data('list',l)
    del_files()
    display_files()

#shows the window for saving the output
def merger(sender,data):
    l = get_data('list')
    s = filesavebox(title="Opslaan als", default='output.pdf', filetypes="*.pdf")
    merge(l, s)

#clear list
def del_files():
    delete_item('lijst')

#callback for up button
def b_up(sender,data):
    l = get_data('list')
    l = verplaats(l, data, 'u')
    add_data('list', l)
    del_files()
    display_files()

#callback for down button
def b_down(sender,data):
    l = get_data('list')
    l = verplaats(l, data, 'd')
    add_data('list', l)
    del_files()
    display_files()

#callback for delete button
def b_del(sender,data):
    l = get_data('list')
    del l[data]
    add_data('list', l)
    del_files()
    display_files()

#displays the items in the list on the gui
def display_files():
    l = get_data('list')
    with child('lijst', parent='main'):
        for i in range(len(l)):
            name = l[i]["name"]
            with child('c'+name, height=33):
                add_text(name)
                add_same_line(xoffset=300)
                add_button('up##'+name, enabled=i!=0, callback=b_up, callback_data=i)
                add_same_line()
                add_button('down##'+name, enabled=i!=len(l)-1, callback=b_down, callback_data=i)
                add_same_line()
                add_button('del##'+name, callback=b_del, callback_data=i)
    
#initialize the gui
def gui():
    l = []
    add_data('list', l)
    set_theme("Gold")
    with window("main"):
        with menu_bar("Menu"):
            add_menu_item("add file", callback=add_file)
            add_menu_item("add folder", callback=add_folder)
            add_menu_item("merge", callback=merger)
        display_files()
    set_main_window_size(600,800)
    set_main_window_title("pdf samenvoeger")
    start_dearpygui(primary_window='main')


if __name__ == "__main__":
    gui()

