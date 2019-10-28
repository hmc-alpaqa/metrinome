from flask import Flask 

app = Flask(__name__) 

@app.route('/convert', methods=["POST"])
def do_covert():
    '''
    ''' 
    return None

@app.route('/metrics', methods=["POST"])
def do_metrics():   
    '''
    '''
    return None

@app.route('/analyze', methods=["POST"])
def do_analyze(): 
    '''
    '''
    return None

if __name__ == "__main__":
    app.run(debug=True)

