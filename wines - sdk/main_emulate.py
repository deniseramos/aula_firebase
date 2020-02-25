from flask import Flask, request
from main import wines

app = Flask('functions')
methods = ['GET','POST','PUT','DELETE']
@app.route('/wines', methods=methods)
@app.route('/wines/<func>', methods=methods)
@app.route('/wines/<func>/<no>', methods=methods)
def catch_all(func='', no=''):
	request.path = '/' + func + '/' + no
	return wines(request)
if __name__== '__main__':
	app.run()





