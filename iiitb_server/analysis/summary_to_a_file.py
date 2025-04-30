from datetime import datetime
class write_to_file: 
    def write(self,path, data):
        now = datetime.now()
        new_data  = "Time :"+str(now)+"\n\n"+data
        with open(path, 'w') as file:
            file.write(new_data)
        

    
