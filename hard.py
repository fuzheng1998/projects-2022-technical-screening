"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge. 
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json
import re

courses_pattern = '[A-Z]{4}[0-9]{4}'
keywords_pattern = 'or|OR|and|AND|in'
credit_pattern = '\d+ units'
level_pattern = 'level \d \w{4} courses'
brackets_pattern = '\(|\)'


def tokenize(input: str):
    pattern = level_pattern + '|' + courses_pattern + '|' + keywords_pattern + '|' + credit_pattern + '|' + brackets_pattern
    import re
    print('tokenized: ', re.findall(pattern, input))
    return re.findall(pattern, input)


operatorDict = {
    'or': 0,
    'and': 1,
    'in': 2,
    'OR': 0,
    'AND': 1,
    'IN': 2,
    '(': 10000,
    ')': 10000
}


def isLevelOf(courseNum: str, level: str):
    if re.match(pattern='[A-Z]{4}' + level, string=courseNum):
        return True
    else:
        return False


def isOprands(token) -> bool:
    if re.match(keywords_pattern + '|' + brackets_pattern, token):
        return False
    return True


def isStudied(course: str, studied_list: list):
    if course in studied_list:
        return True
    else:
        return False


def basicCalculate(left: bool, op: str, right: bool) -> bool:
    res = 0
    if op == 'or' or op == 'OR':
        res = left or right
    elif op == 'and' or op == 'AND':
        res = left and right
    print(res)
    return res


def calculate(studied_list: list, rpn_expr: list):
    # rpn_expr = reversePolishOf(tokenized_ls=requirements1)
    # stack element is True/False
    res_stack = []

    for i in rpn_expr:
        if isOprands(i):
            # if just course
            res_stack.append(isStudied(i, studied_list))
        else:
            # if meet and/or
            op1 = res_stack.pop()
            op2 = res_stack.pop()
            res = basicCalculate(left=op1, op=i, right=op2)
            if i == len(rpn_expr) - 1:
                return res
            else:
                res_stack.append(res)
    print('res_stack in calculate()', res_stack)
    return res_stack


def reversePolishOf(tokenized_ls: list):
    """
    generate reverse Polish e.g. 2*5 -> 25*
    :param tokenized_ls:
    :return: reverse_polish:list
    """
    opStack = []
    res_list = []
    for i in tokenized_ls:
        # if not keywords, add to result list
        if isOprands(i):
            res_list.append(i)
        else:
            # if keywords,
            # if stack empty, add to stack
            if len(opStack) == 0:
                opStack.append(i)
            else:
                # brackets
                if i == '(':
                    opStack.append(i)
                elif i == ')':
                    while (True):
                        popped_op = opStack.pop()
                        if popped_op == '(':
                            break
                        else:
                            res_list.append(popped_op)
                else:
                    top_of_opStack = opStack[-1]
                    tmp_priority = operatorDict[i]
                    top_stack_priority = operatorDict[top_of_opStack]
                    if tmp_priority > top_stack_priority:
                        opStack.append(i)
                    else:
                        while tmp_priority >= top_stack_priority:
                            res_list.append(opStack.pop())
                            if len(opStack) == 0:
                                break
                            if opStack[-1] == '(':
                                break
                        opStack.append(i)

    while len(opStack) != 0:
        res_list.append(opStack.pop())
    print('reversed polish: ', res_list)
    return res_list


# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()


def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """

    # TODO: COMPLETE THIS FUNCTION!!!
    print('requirement: ', CONDITIONS[target_course])
    if len(CONDITIONS[target_course]) == 0:
        return True
    else:
        rpn = reversePolishOf(tokenized_ls=tokenize(CONDITIONS[target_course]))
        res = calculate(studied_list=courses_list, rpn_expr=rpn)

    return res[0]


if __name__ == '__main__':
    import test_hard

    test_hard.test_single()
    test_hard.test_empty()
    test_hard.test_compound()
    pass
