class Test:
    def __init__(self,a=1) -> None:
        self.a=a
    
    def get(self):
        print(self.a)
    # cls + '(website="' + website + '")'
d='4'
a=eval("Test"+'(a="'+d+'")')
a.get()
    