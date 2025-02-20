'''
Unit tests for Message
'''
from datetime import datetime
import uuid
from idmefv2.message import Message, SerializedMessage

VERSION = '2.D.V03'

def now():
    '''Returns current date and time'''
    return datetime.now().isoformat('T')

def new_uuid():
    '''Returns a UUID 4'''
    return str(uuid.uuid4())

def message1():
    '''Returns a test message'''
    msg = Message()
    msg['Version'] = VERSION
    msg['ID'] = new_uuid()
    msg['CreateTime'] = now()
    msg['Analyzer'] = {
        'IP':'127.0.0.1',
        'Name':'foobar',
        'Model':'generic',
        'Category':['LOG'],
        'Data':['Log'],
        'Method':['Monitor'],
    }
    return msg


def message2():
    '''Returns a test message'''
    msg = Message()
    msg['Version'] = VERSION
    msg['ID'] = new_uuid()
    msg['CreateTime'] = now()
    msg['Analyzer'] = {
        'IP':'127.0.0.1',
        'Name':'foobar',
        'Model':'generic',
        'Category':['LOG'],
        'Data':['Log'],
        'Method':['Monitor'],
    }
    msg['Sensor'] = [
        {
            'IP':'192.168.1.1',
            'Name':'TheSensor',
            'Model':'TheSensorModel',
        },
        {
            'IP':'192.168.1.2',
            'Name':'TheSensor2',
            'Model':'TheSensor2Model',
        },
    ]
    return msg

def json1() -> bytes:
    '''Returns a test JSON string'''
    return b'''{
        "Version":"2.D.V03",
        "CreateTime":"2021-11-22T14:42:51.881033Z",
        "ID":"09db946e-673e-49af-b4b2-a8cd9da58de6",
        "Analyzer":{
            "Category":["LOG"],
            "IP":"127.0.0.1","Model":"generic",
            "Data":["Log"],
            "Method":["Monitor"],
            "Name":"foobar"
            }
        }'''

def test_message1():
    '''Test if message is valid'''
    message1().validate()

def test_message2():
    '''Test if message is valid'''
    message2().validate()

def test_serialize_message1():
    '''Test serialization/deserialization of a message'''
    pelode = message1().serialize("application/json")
    message = Message.unserialize(pelode)
    assert message['Version'] == VERSION

def test_unserialize_json1():
    '''Test deserialization of a JSON string'''
    pelode = SerializedMessage("application/json", json1())
    message = Message.unserialize(pelode)
    assert message['Analyzer']['Category'][0] == 'LOG'
