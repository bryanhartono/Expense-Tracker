from datetime import date

class Record:
    '''
    This class contains three getter methods for each of the attributes that will be initialized from
    the parameters passed. Purpose of this class is to be able to represent a record.
    '''
    def __init__(self, Date, category, description, amount):
        '''
        This is the class constructor. Initializes three attributes from the parameters 'Date', 'category',
        'description', and 'amount'.
        '''
        self._date = Date
        self._category = category
        self._description = description
        self._amount = amount

    @property
    def Date(self):
        '''getter method for self._date'''
        return self._date

    @property
    def category(self):
        '''getter method for self._category'''
        return self._category

    @property
    def description(self):
        '''getter method for self._description'''
        return self._description

    @property
    def amount(self):
        '''getter method for self._amount'''
        return self._amount

class Records:
    def __init__(self):
        '''
        This is the class constructor. Its function is for loading up the previous existing record from the file
        'records.txt' and append them to desc_list and money_left if the record exists, if not it will prompt the
        user to enter a new amount for money_left.
        '''
        self._desc_list = []
        try:
            fh = open('records.txt', 'r') # Opens previous record
            try:
                self._money_left = int(fh.readline()) # Reads balance in first line
                # Reading the previous record
                for i in fh.readlines():
                    temp = i.split(' ')
                    temp[3] = int(temp[3])
                    self._desc_list.append(Record(temp[0], temp[1], temp[2], temp[3]))
            except ValueError:
                self._money_left = 0 
            fh.close()
        except FileNotFoundError:
            self._money_left = 0
    
    
    def get_rec(self):
        '''
        This function will return each and every existing records that have been added by the user in the form of
        a list.
        '''
        tmp = []
        for i in self._desc_list:
            tmp.append(f'{i.Date:<14}{i.category:<14}{i.description:<14}{i.amount:<14}')
        return tmp
    
    @property
    def get_bal(self):
        '''
        This property function is used mostly for showing the user how much money is currently left inside his/ her
        balance. 
        '''
        return self._money_left
    
    def update_bal(self, value):
        '''
        This function is for updating the value of the user's balance, namely self._money_left. There is one parameter
        that needs to be passed on to this function and that is the new value for the user's balance.
        '''
        self._money_left = value
        for i in self._desc_list:
            self._money_left += i.amount
        
    def get_added(self):
        '''
        This function will return the user's last added record, which will then be inserted into the list of records in
        the result listbox for the user to see and verify.
        '''
        x = self._desc_list[-1]
        x_str = f'{x.Date:<14}{x.category:<14}{x.description:<14}{x.amount:<14}'
        return x_str
        
    def add(self, expense_income, category):
        '''
        This function takes in the two parameters, the first one is a record and the 
        second one is the instantiation made from the Categories class . the instantiation
        is needed because the function 'is_category_valid' will be called to check the
        category parameter that the user input in. the record will then be added to
        'desc_list' and the amount will be added to 'money_left'.
        '''
        try:
            temp = expense_income.split(' ')
             
            '''checks if user inputted a date or no.'''
            if len(temp) != 4:
                '''If not then set date as today's date.'''
                temp.insert(0, date.today())
            else:
                try:
                    '''checks the format of the date inputted.'''
                    temp[0] = date.fromisoformat(temp[0])
                except:
                    print('The format of date should be YYYY-MM-DD.\nFail to add a record.')
                    return

            check = category.is_category_valid(temp[1])
            if check != True:
                raise NameError
            else:
                temp[3] = int(temp[3])
                self._money_left += temp[3]
                self._desc_list.append(Record(str(temp[0]), temp[1], temp[2], temp[3]))
        # If input cannot be split into with ' '
        except IndexError:
            print("Please try again, the format of the record should be 'description amount'")
        # If temp[1] cannot be converted into integer
        except ValueError:
            print('Invalid value for money. Fail to add a record.')
        # If category is not in the category list
        except NameError:
            print('The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')

    def delete(self, delete_record):
        '''
        This function has only one parameters that needs to be passed onto. That parameter is an index which will be used to find
        which record the user wants to delete. Then the function will delete that specific record and update the user's balance.
        '''
        self._money_left -= self._desc_list[delete_record].amount
        self._desc_list.pop(delete_record)

    def find(self, target_categories):
        '''
        This function has one parameter that needs to be passed onto which is a category. 
        After that, this function will find all the records in the specified category or in a
        subcategory under it. Then the function will print out all the records under the 
        specified category or subcategory if there are any, if there is no record under the 
        specified category, the function will print an empty table.
        '''
        filtered_list = list(filter(lambda x: x.category in target_categories, self._desc_list))
        sum_money = 0 # for total amount of money in the chosen category
        tmp = []
        
        for i in filtered_list:
            sum_money += i.amount # adds amount to sum of money
            tmp.append(f'{i.Date:<14}{i.category:<14}{i.description:<14}{i.amount:<14}')

        return tmp, sum_money

    def save(self):
        '''
        This function will write all existing records to the file 'records.txt' so that when the
        user executes the program again, the user does not have to start from the beginning again.
        '''
        with open('records.txt' , 'w') as fh:
            fh.write(str(self._money_left))  # Writes money_left
            fh.write('\n')
            content_list = []   # List for existing record
            for i in self._desc_list:
                content = i.Date + ' ' + i.category + ' ' + i.description + ' ' + str(i.amount) + '\n'
                content_list.append(content)
            fh.writelines(content_list)  # Writes existing record

