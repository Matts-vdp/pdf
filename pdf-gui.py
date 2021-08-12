# contains all gui code and the main function

import os
from dearpygui.dearpygui import *
from easygui import diropenbox, fileopenbox, filesavebox
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from pdf import PdfList

#shows the window for adding a file to the list
def add_file(sender, app, data):
    f = fileopenbox(title="Kies een file", default='*.pdf', filetypes="*.pdf", multiple=False)
    if f == None:
        return
    pdfs.addFile(f)
    del_files()
    display_files()
 
#shows the window for adding a folder to the list
def add_folder(sender, app, data):
    path = diropenbox(title="Kies een folder") 
    if path == None:
        return
    pdfs.findFiles(path)
    del_files()
    display_files()

#shows the window for saving the output
def merger(sender, app, data):
    s = filesavebox(title="Opslaan als", default='output.pdf', filetypes="*.pdf")
    if s == None:
        return
    pdfs.merge(s)

#clear list
def del_files():
    delete_item(ui_list)

#callback for up button
def b_up(sender, app, data):
    pdfs.swap(data, True)
    del_files()
    display_files()

#callback for down button
def b_down(sender, app, data):
    pdfs.swap(data, False)
    del_files()
    display_files()

#callback for delete button
def b_del(sender, app, data):
    pdfs.remove(data)
    del_files()
    display_files()

# callback for the split button in the extra window
def split(sender, app, data):
    page = get_value(data['page'])
    pdfid = data['pdf']
    pdfs.split(pdfid, page)
    delete_item(get_item_parent(sender))
    del_files()
    display_files()

#callback for split button
def b_split(sender, app, data):
    with window(label="split " + pdfs.l[data].name, pos=[30,30], autosize=True):
        add_text("Page: ")
        add_same_line()
        pagenum = add_input_int(default_value=1, min_value=1, max_value=pdfs.l[data].getNumPages()-1)
        add_button(label="Split", callback=split, user_data={'page':pagenum, 'pdf':data})

#displays the items in the list on the gui
def display_files():
    with child(label='list', parent=main_window, id=ui_list):
        for i in range(pdfs.size()):
            name = str(pdfs.l[i])
            with child(label='c'+name, height=40, no_scrollbar=True):
                add_text(name)
                add_same_line(xoffset=300)
                add_button(label='up##'+name, enabled=i!=0, callback=b_up, user_data=i)
                add_same_line()
                add_button(label='down##'+name, enabled=i!=pdfs.size()-1, callback=b_down, user_data=i)
                add_same_line()
                add_button(label='del##'+name, callback=b_del, user_data=i)
                add_same_line()
                add_button(label='split##'+name, callback=b_split, user_data=i)
    
#initialize the gui
def gui():
    with theme(default_theme=True) as theme_id:
        add_theme_color(mvThemeCol_Button, (0, 78, 120), category=mvThemeCat_Core)
        add_theme_style(mvStyleVar_FrameRounding, 5, category=mvThemeCat_Core)

    with window(label="main", id=main_window):
        with menu_bar(label="Menu"):
            add_menu_item(label="add file", callback=add_file)
            add_menu_item(label="add folder", callback=add_folder)
            add_menu_item(label="merge", callback=merger)
        display_files()
    setup_viewport()
    set_viewport_title(title='Pdf Tool')
    set_viewport_width(600)
    set_viewport_height(800)
    set_primary_window(main_window, True)
    start_dearpygui()



pdfs = PdfList()
main_window = generate_uuid()
ui_list = generate_uuid()

if __name__ == "__main__":
    gui()
