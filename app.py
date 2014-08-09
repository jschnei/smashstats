from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
        

@app.route("/", methods=['GET', 'POST'])
def main():
    player = None
    msg = ''
    chain = []
    
    if request.method=='POST':
        player = request.form.get('player', '')
        btc = pickle.load(open('static/data/betterthanciz.pkl', 'r'))
        
        chain = btc.get(player,[])
        
        if player == 'C!Z':
            msg = 'No (You are C!Z)'
        elif chain:
            msg = 'Yes'
        else:
            msg = 'No'
        
            

    return render_template('betterthanciz.html', player=player, 
                                                 msg=msg,
                                                 chain=chain)

if __name__ == "__main__":
    app.run(debug=True)