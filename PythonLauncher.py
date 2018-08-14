# encoding: utf-8
import json
import os
import threading
import logging
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
        logging.debug("========starting a new thread========")
        for i in range(0, 10):
            try:
                self.importModule.run(self.parameters)
                break
            except Exception, ex:
                logging.error('Thread creating error: %s try %s temps', ex, i)
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
    logging.debug("Somebody calling in")
    moduleName = fRequest.json.get('cmd')
    parameters = fRequest.json.get('params')
    isSynch = str(fRequest.json.get('isSynch'))
    try:
        modulePath = './plugins/'+moduleName+'.py'
        module = load_source(moduleName, modulePath)
    except Exception, ex:
        logging.error(ex)

        result = '{"result":9,"note":"moduel not exist"}'
        return result
    if isSynch == "false":
        newThread = PythonRunner(module, parameters)
        newThread.start()
        result = '{"result":0,"note":"sending Asynchronously, please check the results later"}'
    else:
        result = module.run(parameters)
    logging.info('Launching module [ %s ]:\nREQ=%s\nRES=%s', moduleName, str(fRequest.json), result)
    return result


if __name__ == '__main__':
    # TODO : change log level in config files
    logging.basicConfig(
        level=logging.NOTSET, format='%(asctime)s [%(levelname)s]\t[%(filename)s:%(lineno)d]: %(message)s')
    app.run(host='0.0.0.0', port=12580)
