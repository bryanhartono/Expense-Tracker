class Categories:
    """
    This class contains all methods that has to do with the record's categories. It can be used to check if
    the category is in the list or no, you can call a method to show the categories and its subcategories
    hierarchically, and others.
    """
    def __init__(self):
        '''
        This is the class constructor which has only one attribute which is the provided categories list. This
        list will be used later on in checking if a category is inside or no, it will be used to show all the
        names of the categories hierarchically, and others.
        '''
        self._categories = ['expense', ['food',['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def is_category_valid(self, category):
        '''
        Using the inner function, this functions checks if the category of a descirption that
        the user wants to add is in the categories list or no. This function checks the list
        recursively as there are subcategories in the list. This will return the value True
        if the category is in the list, otherwise it will return false.
        '''
        def is_val(category, categories):
            '''
            This inner function is a recursive function which will return a boolean value of
            True of False. This function will be executed if the user enters 'add' for the initial
            command. This function will return True if the target category is in the categories list
            and False otherwise. Its recursive case is if the parameter 'categories' passed onto it
            is a list, and it's base case is if 'categories' is not a list.
            '''
            if type(categories) == list:
                p = False
                for i in categories:
                    p = p or is_val(category, i)
                return p
            else:
                return category == categories

        return is_val(category, self._categories)

    def find_subcategories(self, category):
        '''
        Using the inner function, this function takes a category name and the categories
        list and it will return a non-nested list containing the specified category and
        the subcategories under it.
        '''
        def find_subcategories_gen(category, categories, found = False):
            '''
            This is an inner function is a recursive generator which yields the target
            category and its subcategories(if there are any). Its recursive case is if
            the parameter 'categories' passed onto it is a list, and its base case is
            if 'categories' is not a list.
            '''
            if isinstance(categories, list):
                for index, i in enumerate(categories):
                    yield from find_subcategories_gen(category, i, found)
                    if i == category and index + 1 < len(categories) \
                            and isinstance(categories[index+1], list) and found == False:
                                yield from find_subcategories_gen(category, categories[index:index+2], True)
            else:
                if category == categories or found:
                    yield categories

        return [i for i in find_subcategories_gen(category, self._categories, )]

    def view(self):
        '''
        This function returns all the provided categories hierarchically for the user
        to choose a category when adding a new record.
        '''
        def cat_outline(L, prefix=0):
            '''
            This inner function is a recursive function which will print out the categories
            hierarchically. its recursive case is if L is a list and its base case is if L
            is not a list.
            '''
            if isinstance(L, list):
                tmp = []
                for v in L:
                    tmp.extend(cat_outline(v, prefix+1))
                return tmp
            else:
                s = [' ' * 2 * prefix + L]
                return s
        result = []
        for i in self._categories:
            if isinstance(i, list):
                x = cat_outline(i) # if i is a list then it will be flatten out using the inner function.
                result.extend(x) # insert the flattened categories into the 'result' list.
            else:
                result.append(i)
                
        return result
    
