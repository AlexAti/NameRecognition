import sys
sys.path[0] = sys.path[0].replace('NameRecognition\\NameRecognition','NameRecognition')

from NameRecognition.app import app

if __name__ == '__main__':
    app.run()