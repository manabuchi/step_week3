#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type' : 'TIMES'}
    return token, index + 1

def read_divide(line, index):
    token = {'type' : 'DIVIDE'}
    return token, index + 1

def read_startparen(line, index):
    token = {'type' : 'STARTPAREN'}
    return token, index + 1

def read_endparen(line, index):
    token = {'type' : 'ENDPAREN'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_startparen(line, index)
        elif line[index] == ')':
            (token, index) = read_endparen(line, index)        
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
        # print("tokenized!")
    return tokens

def evaluate_expression(tokens, start=0):
    new_tokens = []
    index = start
    while index < len(tokens):
        token = tokens[index]
        if token['type'] == 'STARTPAREN':
            # 再帰で内側の括弧を評価
            sub_tokens, next_index = evaluate_expression(tokens, index + 1)
            value = evaluate_plus_and_minus(evaluate_times_and_divide(sub_tokens))
            new_tokens.append({'type': 'NUMBER', 'number': value})
            index = next_index
        elif token['type'] == 'ENDPAREN':
            return new_tokens, index + 1
        else:
            new_tokens.append(token)
            index += 1
    return new_tokens, index

def evaluate_times_and_divide(tokens):
    new_tokens = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token['type'] == 'NUMBER':
            current_value = token['number']
            while (index + 1 < len(tokens) and tokens[index + 1]['type'] in ('TIMES', 'DIVIDE')):
                symbol = tokens[index + 1]['type']
                next_number = tokens[index + 2]['number']
                if symbol == 'TIMES':
                    current_value *= next_number
                elif symbol == 'DIVIDE' and next_number== 0:
                    # print("ZeroDivisionError")
                    return None 
                else:
                    current_value /= next_number
                index += 2 # 演算子と次の数値をスキップ
            new_tokens.append({'type': 'NUMBER', 'number': current_value})
        elif token['type'] in ('PLUS', 'MINUS'):
            new_tokens.append(token)
        else:
            print('Invalid syntax')
            exit(1)
        index += 1
    # print(new_tokens)
    return new_tokens

def evaluate_plus_and_minus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    tokens = tokenize(line)
    evaluated_tokens, _ = evaluate_expression(tokens)
    second_answer = evaluate_times_and_divide(evaluated_tokens)
    if second_answer is None:
        print("ZeroDivisionError")
        return
    actual_answer = evaluate_plus_and_minus(second_answer)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1")
    test("1+2")
    test("1.0+2")
    test("1.0+2.0")
    test("1*2")
    test("1.0*2")
    test("4/2")
    test("4/0")              # divide by zero
    test("4.0/2")
    test("4.0/2.0")
    test("3/2")
    test("1/100")
    test("3+4/2")
    test("3.0+4*2")
    test("3.0+4*2-1/5")
    test("1.0+2.1-3")
    # with parenthesis
    test("(1+2)")
    test("(3+4)*2")
    test("1+(2*3)")
    test("((1+2)*3)")
    test("4*(5+6)/2")
    test("((1+1)+(2+2))")
    test("((1+2)*(3+4))/5")
    test("1+(2+(3+(4+5)))")
    test("(1+(2*(3+(4*5))))")
    test("(((((((1)))))))")    
    test("1 + ((2 + 3) * (4 + 5))")
    test("1 + (2 + 3 * (4 + (5 - 6)))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    evaluated_tokens, _ = evaluate_expression(tokens)
    second_tokens = evaluate_times_and_divide(evaluated_tokens)
    if second_tokens is None:
        print("ZeroDivisionError\n")
        continue
    answer = evaluate_plus_and_minus(second_tokens)
    print("answer = %f\n" % answer)