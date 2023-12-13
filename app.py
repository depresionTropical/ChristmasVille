from flask import Flask, render_template, request
from smbus import SMBus

bus = SMBus(1) 
estados = [False,False,False,False,False]

encendido = "Estrella"
apagado = "Inicio"

tokenList = ["1","2","3","4","5"]
addrs = [0x09,0x08,0x0A,0x0B,""]


app = Flask(__name__)

def solicitarToken(addrs,token,sk,n):
    if addrs == 0x08:
        if sk == token:
            try:
                bus.write_byte(addrs,1)
                estados[n] = True
            except:
                estados[n] = True
        else:
            try:
                bus.write_byte(addrs,90)
                estados[n] = False
            except:
                estados[n] = False
    else:
        if sk == token:
            try:
                bus.write_byte(addrs,1)
                estados[n] = True
            except:
                estados[n] = True
        else:
            try:
                bus.write_byte(addrs,0)
                bus.write_i2c_block_data(0x0A,0,[ord(c) for c in apagado])
                estados[n] = False
            except:
                estados[n] = False



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar/<v>',methods=['POST'])
def procesar(v):
    n = int(v)
    texto_ingresado = request.form['texto']
    solicitarToken(addrs[n],tokenList[n],texto_ingresado,n)
    #print(f"{v}: {texto_ingresado}")
    return render_template('index.html')

@app.route('/estrella')
def estrella():
    print(estados)
    if estados[0] and estados[1] and estados[2] and estados[3] and estados[4]:
        bus.write_i2c_block_data(0x0A,0,[ord(c) for c in encendido])
    """    
    else:
        bus.write_i2c_block_data(0x0A,0,[ord(c) for c in apagado])
    """

    return render_template('index.html')

if __name__ == '__main__':
    #bus.write_i2c_block_data(0x08,0,[ord(c) for c in apagado])
    app.run(debug=True)
    for add in addrs:
        try:
            bus.write_byte(add,0)
        except:
            pass
    bus.write_i2c_block_data(0x0A,0,[ord(c) for c in apagado])
    bus.write_byte(addrs[1],90)
    
    #bus.write_byte(0x08,0)
