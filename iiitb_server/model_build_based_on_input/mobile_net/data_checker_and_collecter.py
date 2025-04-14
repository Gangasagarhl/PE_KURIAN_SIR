class data_check_and_download:
    def __init__(self,database = 'database', names_list=[]):
        self.database  =  database
        self.names_list=names_list
        
        
    def check_the_data_is_avaialble_in_database(self):
        not_present=[]
        import os
        names_in_director = os.listdir(self.database)
        for i in self.names_list:
            if i  not in names_in_director:
                not_present.append(i)
        return not_present
    
        
    
    def download_300_image_from_google_and_store_database(self): 
        
        pass
    
    def fine_tune_mobile_net_small_model_pass_it_to_appropriate_user(self):
        pass
        