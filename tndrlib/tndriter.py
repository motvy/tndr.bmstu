class MyIter:
    def __init__(self, input_list):
        self.input_list = list(input_list)

        self.indx = 0
        self.max_indx = len(input_list)
    
    def next(self):
        self.indx += 1
        if self.indx == self.max_indx:
            self.indx = 0
        
        current_el = self.input_list[self.indx]

        return current_el
    
    def item(self):
        current_el = self.input_list[self.indx]

        return current_el
    
    def prev(self):
        self.indx -= 1
        if self.indx == -1:
            self.indx = self.max_indx - 1

        current_el = self.input_list[self.indx]

        return current_el
    
    def remove(self, el):
        try:
            current_indx = self.input_list.index(el)
            self.input_list.remove(el)
        except Exception as err:
            if 'x not in list' in str(err) or 'is not in list' in str(err):
                pass
            else:
                raise err
        else:
            if current_indx <= self.indx:
                self.indx -= 1
            self.max_indx = len(self.input_list)
            if self.max_indx == 0:
                raise Exception("Iterator is empty")
