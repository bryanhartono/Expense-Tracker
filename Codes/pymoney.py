import tkinter
from tkinter.ttk import *
from pycategory import Categories
from pyrecord import Records
from datetime import date
import os
if os.environ.get('DISPLAY','') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

count = 1 # For records

def Reset():
    '''
    sets all tkinter.StringVar and tkinter.Entry to an empty string, but still show the records that had already
    been added by the user and his/her money balance.
    '''
    global find_cat_pat, date_val, des_val, cat_val, amt_val, result_box, date_entry, amt_entry, des_entry, count, update_value, money_label
    count = 1
    find_cat_pat.set('')
    date_val.set('')
    cat_val.set('')
    des_val.set('')
    amt_val.set('')
    result_box.delete(0, 'end')
    date_entry.configure(state = tkinter.NORMAL)
    amt_entry.configure(state = tkinter.NORMAL)
    des_entry.configure(state = tkinter.NORMAL)
    update_value.set('')
    money_label.configure(text = 'Now you have %d dollars.' % records.get_bal)
    for i in records.get_rec():
        result_box.insert(count, i)
        count += 1

def zero_money():
    '''
    This function is called when the user presses the 'Reset balance' button. If called, then this function will
    set the value of the user's money balance to 0 allowing him/her to update the initial value'
    '''
    global money_label, update_entry
    zero = 0
    records.update_bal(int(zero))
    money_label.configure(text = 'Now you have %d dollars.' % records.get_bal)
    update_entry.configure(state = tkinter.NORMAL)
    
def find_cat():
    '''
    This function is called after the user presses the 'Find' button and he/she had chosen the category of records
    that he/she wants to see. if called, this function will get the value of what the user chosen and call the 
    find_subcategories method from the categories class to check if there are any subcategories under the category
    that the user had chosen. then this function will call the find method from the records class and return the values
    to the variables found, which is all of the records in the chosen category, and sum_money, which is the total sum
    of the amount of these records. Then the records will be inserted into the list_box and the function will update
    the money balance written at the bottom left of the frame.
    '''
    global find_cat_pat, result_box, money_left, money
    category = find_cat_pat.get()
    
    if len(category) > 0:
        if categories.is_category_valid(category):
            result_box.delete(0, 'end')
            sub_cat = categories.find_subcategories(category)
            found, sum_money = records.find(sub_cat)
            count = 1
            for i in found:
                result_box.insert(count, i)
                count += 1
            money_label.configure(text = 'Now you have %d dollars.' % sum_money)
    else:
        '''
        If the user does not enter any category, then the function will show all existing records that had been added.
        '''
        result_box.delete(0, 'end')
        count = 1
        for i in records.get_rec():
            result_box.insert(count, i)
            count += 1
    
def delete():
    '''
    This function is called if the user presses the 'Delete' button. If called, then the function will delete the selected
    record from both the result_box and from the record and the user's money balance will be updated by calling the
    get_bal method from the records class.
    '''
    global result_box, count, money_label
    choice = result_box.curselection()
    if len(choice) > 0:
        for i in choice:
            records.delete(i)
            result_box.delete(i)
            count -= 1
            money_label.configure(text = 'Now you have %d dollars.' % records.get_bal)
    else:
        return
    
def initial_bal():
    '''
    This function is called when the user presses the update button after entering a value into the update_entry.
    if called it will first check if the value entered is an integer. If it is then the function will call the 
    update_bal from the records class to first update the user's money balance then it will call the get_bal method
    from the records class to get the value of the current money balance. Then this function will disable the entry
    for updating the initial money value unless the 'Reset balance' button is pressed.
    '''
    global update_value, money_label, update_entry
    val = update_value.get()
    if val == None:
        return
    try:
        x = val
        x = int(x)
    except ValueError:
        tkinter.messagebox.showerror('','Invalid amount format.\nPlease enter an integer.')
        update_value.set('')
        return
    val = int(val)
    records.update_bal(val)
    money_label.configure(text = 'Now you have %d dollars.' % records.get_bal)
    update_value.set('')
    if records.get_bal != 0:
        update_entry.configure(state = tkinter.DISABLED) 
    
def add():
    '''
    This function is called when the user presses the 'add a record' button and all the entries above the button had
    been filled with the appropraite format and value. If the date inputted is not using the correct format the record
    will not be added. If the category inputted or the user does not choose any category from the combobox, then the
    record will not be added. If the amount inputted is not an integer, the record will not be added. If all these 
    conditions are fulfilled, then this function will passed on the inputted values onto the add method in the records
    class and it will insert the record inputted into the result_box and also update the user's money balance.'
    '''
    global amt_val, des_val, cat_val, date_val, count, result_box, money_label
    
    category = cat_val.get().replace(" ", "")
    description = des_val.get()
    amount = amt_val.get()
    Date = date_val.get()
    
    tmp = description.split(' ')
    if len(tmp) > 1:
        tkinter.messagebox.showerror('','Invalid description format.\nPlease enter a single word description.')
        date_val.set('')
        cat_val.set('')
        des_val.set('')
        amt_val.set('')
        return
    if len(Date) > 0:
        try:
            Date = date.fromisoformat(Date)
        except ValueError:
            tkinter.messagebox.showerror('','Invalid date format.\nDate format: YYYY-MM-DD.')
            date_val.set('')
            cat_val.set('')
            des_val.set('')
            amt_val.set('')
            return
        else:
            records.add(' '.join([str(Date), category, description, amount]), categories)
    elif len(category) > 0 and len(description) > 0 and len(amount) > 0:
        if categories.is_category_valid(category):
            try:
                n = amount
                n = int(n)
            except ValueError:
                tkinter.messagebox.showerror('','Invalid amount format.\nPlease enter an integer.')
                date_val.set('')
                cat_val.set('')
                des_val.set('')
                amt_val.set('')
                return
            else:
                records.add(' '.join([category, description, amount]), categories)
        else:
            tkinter.messagebox.showerror('','Invalid category!\nPlease choose from the available cateogry.')
            date_val.set('')
            cat_val.set('')
            des_val.set('')
            amt_val.set('')
            return
    else:
        return
    money_label.configure(text = 'Now you have %d dollars.' % records.get_bal)
    result_box.insert(count, records.get_added())
    count += 1
    date_val.set('')
    cat_val.set('')
    des_val.set('')
    amt_val.set('')

# Instantiate records
records = Records()
# initializes categories
categories = Categories()

# GUI codes
root = tkinter.Tk()
root.title("Pymoney")


# LEFT SIDE OF FRANE

# Frame
left_f = tkinter.Frame(root, bg = 'SlateGray1', width = 800, height = 350)
left_f.grid(row=0, column=0, sticky = 'ew')

# 'find category' label
find_cat_lab = tkinter.Label(left_f, bg = 'SlateGray1', text = 'find category', width = 18, height = 1)
find_cat_lab.grid(row=0, column=0)
# to input the category
find_cat_pat = tkinter.StringVar()
cat_pat_entry = tkinter.Entry(left_f, textvariable= find_cat_pat, width = 35)
cat_pat_entry.grid(row=0, column=1, padx=5)
# 'Find' button
find_btn = tkinter.Button(left_f, text= 'Find', width = 8, command= find_cat)
find_btn.grid(row=0, column=2)
# 'Reset' button
reset_btn = tkinter.Button(left_f, text= 'Reset', width = 8, command= Reset)
reset_btn.grid(row=0, column=3)

# Scrollbar for the listbox
scrollbar = tkinter.Scrollbar(left_f, orient = 'vertical')
scrollbar.grid(row = 1, column = 5, rowspan = 7, sticky = 'ns')
# listbox for the records
result_box = tkinter.Listbox(left_f, yscrollcommand = scrollbar.set)
result_box.grid(row=1, column=0, rowspan= 7, columnspan= 5, sticky='ew', padx = 3, pady=3)
for i in records.get_rec():
    result_box.insert(count, i)
    count += 1
scrollbar.config(command = result_box.yview)

# label to show user's current money balance
money_label = tkinter.Label(left_f, text = 'Now you have %d dollars' % records.get_bal, bg = 'SlateGray1', width = 23, height = 1)
money_label.grid(row=8, column=0)
# 'Reset balance' button
money_reset = tkinter.Button(left_f, text = 'Reset balance', height=1, width = 12, command = zero_money)
money_reset.grid(row=8, column=2)
# 'Delete' button
del_btn = tkinter.Button(left_f, text = 'Delete', height=1, width = 8, command = delete)
del_btn.grid(row=8, column=3)

# RIGHT SIDE OF FRAME

# 'Initial money' label
update_money = tkinter.Label(left_f, bg='SlateGray1', text= 'Initial money', width=10, height=1)
update_money.grid(row=0, column=6)
# StringVar for initial value
update_value = tkinter.StringVar()
# Entry for initial value
update_entry = tkinter.Entry(left_f, textvariable= update_value, width=30)
update_entry.grid(row=0, column=7, sticky='ns', padx=3, pady=3)
if records.get_bal > 0:
    update_entry.configure(state = tkinter.DISABLED)
# 'Update' button
update_btn = tkinter.Button(left_f, text = 'Update', width=10, height =1, command= initial_bal)
update_btn.grid(row=0, column=8, sticky = 'ns', padx = 3)

# 'Date' label
date_label = tkinter.Label(left_f, text= 'Date', bg='SlateGray1', width=10, height=1)
date_label.grid(row=3, column=6)
# StringVar for date
date_val = tkinter.StringVar()
# Entry for inputting date
date_entry = tkinter.Entry(left_f, textvariable=date_val, width=25)
date_entry.grid(row=3, column=7)

# 'Category' label
category_label = tkinter.Label(left_f, text= 'Category', bg='SlateGray1', width=10, height=1)
category_label.grid(row=4, column=6)
# StringVar for category
cat_val = tkinter.StringVar()
# Entry for category
category_box = tkinter.ttk.Combobox(left_f, width=25, textvariable= cat_val)
category_box['values'] = tuple(categories.view())
category_box.grid(row=4, column=7)

# 'Description' label
des_label = tkinter.Label(left_f, text= 'Description', bg='SlateGray1', width=10, height=1)
des_label.grid(row=5, column=6)
# StringVar for description
des_val = tkinter.StringVar()
# Entry for description
des_entry = tkinter.Entry(left_f, textvariable=des_val, width=25)
des_entry.grid(row=5, column=7)

# 'Amount' label
amt_label = tkinter.Label(left_f, text= 'Amount', bg='SlateGray1', width=10, height=1)
amt_label.grid(row=6, column=6)
# StringVar for amount
amt_val = tkinter.StringVar()
# Entry for amount
amt_entry = tkinter.Entry(left_f, textvariable=amt_val, width=25)
amt_entry.grid(row=6, column=7)

# 'Add a record' button
add_btn = tkinter.Button(left_f, text='Add a record', width=10, command= add)
add_btn.grid(row=7, column=7)

# 'Exit' button
exit_btn = tkinter.Button(left_f, text= 'Exit', width = 8, height = 1, command= root.destroy)
exit_btn.grid(row=8, column=7, padx=5)

tkinter.mainloop()
# Calls save method from records class to save the current record into records.txt 
records.save()
