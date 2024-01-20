import pickle


file_source = open("url.dat", "rb")  
continuer = True
while continuer :
    try  : 
            file_source.seek(0)
            data = pickle.load(file_source)
            print(data) 
         
    except Exception as e :
        raise e
        continuer = False
    

file_source.close()