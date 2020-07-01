#valtyr
import manipulator as m
import json

def create_glyph(glyph):
    data={}
    counter=0
    data['Layers']=len(glyph.layers)
    data['Format']=glyph.file_format
    for layer in glyph.layers:
        data['Layer-'+str(counter)]=layer.get_json()
        counter=counter+1

    m.write_file('crypto.glyph',json.dumps(data))
    #ENCRYPT CRYPTO.GLYPH WITH PASSWORD AFTER DATA WRITE
    return

class layer:
    def get_json(self):
        return {"op":self.operation,"key":self.key,"tag":self.tab,"nonce":self.nonce}

    def add_all(self,operation,key,tab,nonce):
        self.add_op(operation)
        self.add_key(key)
        self.add_tab(tab)
        self.add_nonce(nonce)

    def add_some(self,operation,key):
        self.add_op(operation)
        self.add_key(key)

    def add_op(self, operation):
        self.operation=operation
    
    def add_key(self,key):
        try:
            self.key=m.to_string(key)
        except:
            self.key=key

    def add_tab(self,tab):
        self.tab=tab
    
    def add_nonce(self,nonce):
        self.nonce=nonce

    key=None
    operation=None
    tab=None
    nonce=None


class glyph:
    def add_date(self,date):
        self.date_lock=date

    def add_format(self,file_format):
        self.file_format=file_format

    def add_layer(self,layer):
        self.layers.append(layer)

    def add_password(self,password):
        self.password=password

    layers=[]    
    file_format=None
    password=None
    date_lock=None
