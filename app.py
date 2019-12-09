from numpy import int64
import flask
import pickle
import os
import pandas as pd

port = int(os.getenv("PORT", 9099))
app = flask.Flask(__name__, template_folder='./')

#with open(f'linearmodel.pkl', 'rb') as f:
#        model = pickle.load(f)


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))
    if flask.request.method == 'POST':
        pass
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
    app.run(host='localhost', port=port)
