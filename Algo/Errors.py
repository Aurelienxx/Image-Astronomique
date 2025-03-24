# Code réaliser par : 
#   Dusannier Léothen
#   Fontaine Aurélien 

class MyError(Exception):
    def __init__(self,message="default"):
        super().__init__(message)
    
    