import time
class resource:
    def __init__(self):
        self.__map={}

    def adding(self,key_to_add,value_to_add):
        if key_to_add not in self.__map:
            self.__map[key_to_add]=[value_to_add]
        else:
            self.__map[key_to_add].append(value_to_add)

    def delete(self,key):
        if key in self.__map:
            time.sleep(0)#it should me more than 5 mins
            del self.__map[key]

        



    def print_map(self):
        print(self.__map)


if __name__=="__main__":
    res = resource()
    res.adding("sag","v1")
    res.adding("sag","v2")
    res.print_map() 
    res.adding("sag2", "v3")
    res.print_map()
    res.delete("sag2")   
    print("\n\n")  
    res.print_map()  