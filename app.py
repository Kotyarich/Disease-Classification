from numpy import int64
import flask
import pickle
import os
import pandas as pd
import numpy as np

port = int(os.getenv("PORT", 9099))
app = flask.Flask(__name__, template_folder='./')

#with open(f'linearmodel.pkl', 'rb') as f:
#        model = pickle.load(f)

def poop(string):
    if string == 'неопределено': return (0, 0)
    if string == 'нет': return (0, 1)
    if string == 'да': return (1, 0)
    print('poop')

def poops(string):
   if string == '': return [0, 0, 0, 0, 0]
   if string == 'низко': return [1, 1, 0, 0, 0]
   if string == 'умеренно': return [1, 0, 1, 0, 0]
   if string == 'высоко': return [1, 0, 0, 1, 0]
   if string == 'неопределено': return [0, 0, 0, 0, 1]
   print('poops')

def poopm(string):
    if string == 'неопределено': return np.nan
    if string in ('нет', 'неповышен', 'низкий', 'отсутствие'): return 0
    if string in ('да', 'повышен', 'высокий', 'гиперэкспрессия'): return 1
    print('poopm')

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        n =  int(bool(flask.request.form.get('НаличиеОтдаленныхМетастазов', 0)))

        gos = [
            int(bool(flask.request.form.get('ГистологическийТипОпухолиЭпиталиальный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиАденокарцинома', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиПочечноклеточный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиЭндометриоидный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиПаппилярный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиФолликулярный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиГюртклеточный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиМедуллярный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиАнапластический', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиНеэпиталиальный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиНепочечноклеточный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиНеэндометриоидный', 0))),
            int(bool(flask.request.form.get('ГистологическийТипОпухолиНеаденокарцинома', 0))),
        ]

        go = int(any(gos))

        gks = [
            poop(flask.request.form.get('ГистологическийТипКлетокСветлоклеточный')),
            poop(flask.request.form.get('ГистологическийТипКлетокМелкоклеточный')),
            poop(flask.request.form.get('ГистологическийТипКлетокБазальноклеточный')),
            poop(flask.request.form.get('ГистологическийТипКлетокПлоскоклеточный')),
        ]

        gks = [item for sublist in gks for item in sublist]
        gk = int(any(gks))

        s = poops(flask.request.form.get('СтепеньДиффТканиОпухоли'))

        m = [
            poopm(flask.request.form.get('Маркер_cKit')),
            poopm(flask.request.form.get('Маркер_RAS')),
            poopm(flask.request.form.get('Маркер_EGFR')),
            poopm(flask.request.form.get('Маркер_ALK')),
            poopm(flask.request.form.get('Маркер_PD_L1')),
            poopm(flask.request.form.get('Маркер_BRAF')),
            poopm(flask.request.form.get('Маркер_эстроген')),
            poopm(flask.request.form.get('Маркер_прогестерон')),
            poopm(flask.request.form.get('Маркер_индекс')),
            poopm(flask.request.form.get('Маркер_HER2')),
        ]

        req = [n, go] + gos + [gk] + gks + s + m

        print(n, go, gos, gk, gks, s, m)
        print(req)
        return flask.render_template('main.html', result="req")

        #Education = flask.request.form['Education']
        #Sex = flask.request.form['Sex']
        #Age = flask.request.form['Age']
        #Activity = flask.request.form['Activity']
        #Sport = flask.request.form['Sport']
        #IsAlone = flask.request.form['IsAlone']
        #AgeEducation = flask.request.form['AgeEducation']
        #input_variables = pd.DataFrame([[Education,Sex,Age,Activity,Sport,IsAlone,AgeEducation]],
         #                              columns=['Education','Sex','Age','Activity','Sport','IsAlone','Age*Education'],
        #                               dtype=int64)
        #prediction = model.predict(input_variables)[0]
        #return flask.render_template('main.html',
        #                             original_input={'Education':Education,'Sex':Sex,'Age':Age,'Activity':Activity,'Sport':Sport,'IsAlone':IsAlone,'Age*Education':AgeEducation},
         #                            result=prediction,
         #                            )
if __name__ == '__main__':
    app.run(host='localhost', port=port, debug=True)
