# encoding: utf-8
import json
import os
import threading
from imp import load_source
from flask import Flask, request as fRequest


class PythonRunner(threading.Thread):
    '''
    'Python excute class,using new thread to excute python module.
    TODO: Adding thread name to control thread numbers.
    '''
    def __init__(self, importModule, parameters):
        threading.Thread.__init__(self)
        self.importModule = importModule
        self.parameters = parameters

    def run(self):
        try:
            self.importModule.run(self.parameters)
        except:
            self.stop()
        self.stop()

    def stop(self):
        self.thread_stop = True


app = Flask(__name__)


@app.route('/plugins/launch', methods=['GET'])
def getHelp():
    return 'using templete: {"cmd":"#module name which lays in plugins folder#","params":[#List:module need use#],"isSynch":"#defult true,unless using false#"}"}'


@app.route('/plugins/launch', methods=['POST'])
def startModule():
    if fRequest.json == {}:
        return 'using templete: {"cmd":"#module name which lays in plugins folder#","params":[#List:module need use#],"isSynch":"#defult true,unless using false#"}"}'
    # Detect modules in pulgins folder which 
    print "Somebody calling in with" + str(fRequest.json)
    moduleName = fRequest.json.get('cmd')
    parameters = fRequest.json.get('params')
    isSynch = str(fRequest.json.get('isSynch'))
    try:
        modulePath = './plugins/'+moduleName+'.py'
        module = load_source(moduleName, modulePath)
    except Exception, ex:
        print ex
        return '{"result":9,"note":"moduel not exist"}'
    if isSynch == "false":
        newThread = PythonRunner(module, parameters)
        newThread.start()
        result = '{"result":0,"note":"异步发送中，请稍后查看结果"}'
    else:
        result = module.run(parameters)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12580)
