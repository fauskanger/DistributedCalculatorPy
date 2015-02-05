#!flask/bin/python
import re
from flask import Flask, jsonify, make_response, abort
from enum import Enum


app = Flask(__name__)

Operand = Enum('Operand', 'PLUS MINUS MULTIPLY DIVIDE POWER')

class Expression:
    op1     = 0
    operand = Operand.PLUS
    op2     = 0


@app.route('/api/calc/<expression>', methods=['GET'])
def calculate(expression):

    # Regular expression to validate that the expression is two operators and one operand
    match = re.search(r"^[0-9]+(\.|,)?[0-9]*[\*|\+|\-|\^][0-9]+(\.|,)?[0-9]*", expression)
    if not match:
        abort(400)

    return jsonify({'expression': expression})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)