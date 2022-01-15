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

courses_pattern = r'[A-Z]{4}[0-9]{4}'
keywords_pattern = 'or|OR|and|AND'
credit_pattern = r"\d+ units of credit in level \d|\d+ units of credit in \(.*\)|\d+ units of credit"
level_pattern = r'level \d \w{4} courses'
brackets_pattern = r'\(|\)'
credit_pattern01 = r'(\d+) units of credit'
credit_pattern02 = r'(\d+) units of credit in (level \d+|\(.*\))'


def tokenize(input: str) -> list:
    """
    split str into token phrase with key-info

    :param input: course requirement
    :return: key-info phrase (token)
    """
    input = ' '.join(input.split())
    pattern = credit_pattern + '|' + courses_pattern + '|' + keywords_pattern + '|' + brackets_pattern
    import re
    # print('tokenized: ', re.findall(pattern, input))
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


def isCreditToken(token: str) -> bool:
    """
    whether token is about credit

    :param token: phrase with keyword 'credit'
    :return: Boolean
    """
    if 'credit' in token:
        return True
    else:
        return False


def isLevelOf(course: str, level: str):
    if re.match(pattern='[A-Z]{4}' + level, string=course):
        return True
    else:
        return False


def isOprands(token) -> bool:
    """
    is token of course/credit requirement

    :param token: token split in requirement sentence
    :return: is type like 'XXXX1234' or 'x units of credit'
    """
    if re.match(keywords_pattern + '|' + brackets_pattern, token):
        return False
    return True


def isStudied(course: str, studied_list: list):
    """
    whether the course(str) in token studied

    :param course: course token in
    :param studied_list:
    :return: is course in token studied
    """
    if course in studied_list:
        return True
    else:
        return False


def getLevelX(level: str, studied_ls: list):
    """
    get level x course list from studied course list

    :param level: level number(str) from token
    :param studied_ls: studied courses
    :return: a courses list of specific level in studied course list
    """
    r = re.compile(r"[A-Z]{4}" + level + r"\d{3}")
    level_x = list(filter(r.match, studied_ls))
    return level_x


def basicCalculate(left: bool, op: str, right: bool) -> bool:
    """
    for basic A|B, A&&B calculation

    :param left: a boolean indicating whether Operands meet the requirement
    :param op: AND|and|OR|or
    :param right: similar to left
    :return: calculation result(binary calculation)
    """
    res = 0
    if op == 'or' or op == 'OR':
        res = left or right
    elif op == 'and' or op == 'AND':
        res = left and right
    # print(res)
    return res


def isCredited(credit_token: str, studied_list: list) -> bool:
    """
    parse credit token

    :param credit_token: info with credits, level, course restriction
    :param studied_list: courses studied list
    :return: True/False matching course requirement
    """
    # credit token with 'in'
    if re.match(credit_pattern02, credit_token) is not None:
        # print(re.match(credit_pattern02, credit_token).groups())
        info_group = re.match(credit_pattern02, credit_token).groups()
        credit_units = int(info_group[0])
        # if lower than credit required, must be False
        if len(studied_list) * 6 < credit_units:
            return False
        else:
            # if credit reaches, consider level/course restriction
            level_match01 = re.match(pattern=r'level (\d+)', string=info_group[1])
            level_match02 = re.match(pattern=r'\((.*)\)', string=info_group[1])
            # consider credit token in level X
            if level_match01:
                level: str = level_match01.group(1)
                # get all level x course from course studied list and compare with credit requirement
                level_x_courses: list = getLevelX(level, studied_list)
                studied_credits: int = len(level_x_courses) * 6
                if studied_credits >= credit_units:
                    return True
                else:
                    return False
            elif level_match02:
                #
                course_range: str = level_match02.group(1)
                course_range_ls: list = course_range.split(', ')
                tmp_credit = 0
                for course_studied in studied_list:
                    if course_studied in course_range_ls:
                        tmp_credit = tmp_credit + 6
                if tmp_credit >= credit_units:
                    return True
                else:
                    return False
    elif re.match(credit_pattern01, credit_token) is not None:
        # without 'in', only credit required.
        credit_required = int(re.match(credit_pattern01, credit_token).groups()[0])
        # print('credit_required: ', credit_required)
        if len(studied_list) * 6 < credit_required:
            return False
        else:
            return True
    else:
        raise SyntaxError(credit_token + 'cannot be parsed')


def calculate(studied_list: list, rpn_expr: list):
    """
    To calculate whole RPN(list)

    :param studied_list: courses studied list
    :param rpn_expr: Reversed Polish Notation(list)
    :return: result of True/False in list
    """
    # stack element is True/False
    res_stack = []

    for i in rpn_expr:
        if isOprands(i):
            # if just course
            if isCreditToken(i):
                res_stack.append(isCredited(i, studied_list))
            else:
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
    # print('res_stack in calculate()', res_stack)
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
    # print('reversed polish: ', res_list)
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
    test_hard.test_simple_uoc()
    test_hard.test_annoying_uoc()
    test_hard.test_cross_discipline()
    pass
