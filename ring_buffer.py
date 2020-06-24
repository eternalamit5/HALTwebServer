class RingBuf:
    def __init__(self, size):
        self.size = size
        self.item_list = []

    def append(self, x):
        if len(self.item_list) >= self.size:
            del self.item_list[0]
            self.item_list.append(x)
        else:
            self.item_list.append(x)

        self.print()

    def clear(self):
        self.item_list.clear()

    def print(self):
        for item in self.item_list:
            print(item)