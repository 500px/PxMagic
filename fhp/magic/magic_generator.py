class MagicGenerator(object):
    def __init__(self, iter_source, iter_destination=None):
        self.reset_cache()
        if not iter_destination:
            def do_nothing(thing):
                return thing
            iter_destination = do_nothing
        self.iter_destination = iter_destination
        self.iter_source = iter_source

    def __iter__(self):
        count = 0
        for item in self.cache:
            count += 1
            yield item
        if not count == self.max_length:
            for raw_item in self.iter_source(skip=count):
                count += 1
                item = self.iter_destination(raw_item)
                self.cache.append(item)
                yield item
            self.max_length = count

    def __getitem__(self, number):
        if number < 0:
            needed_items = float('inf')
        else:
            cached_items = len(self.cache)
            needed_items = max(0, number - cached_items + 1)
        generator = (item for item in self)
        while needed_items > 0:
            needed_items -= 1
            try:
                next(generator)
            except StopIteration:
                raise IndexError, "list index out of range"
        return self.cache[number]
    
    def reset_cache(self):
        self.cache = []
        self.max_length = float('inf')
        
    def first(self):
        return self[0]
