# encoding: utf-8

print 'hello world'


def _check_param_num(param):
    if len(param) == 2:
        return True
    else:
        return False


def run(params):
    '''
    Must have, web server will launch the module by the method
    '''
    if _check_param_num(params):
        return '{"result":0}'
    else:
        return '{"result":1,"note":"the number of params is wrong"}'
