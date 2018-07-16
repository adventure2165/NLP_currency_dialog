import sys
from wit import Wit
import requests
from pattern import web

# Quickstart example
# See https://wit.ai/l5t/Quickstart

if len(sys.argv) != 2:
    print("usage: python examples/quickstart.py <wit-token>")
    exit(1)
access_token = sys.argv[1]

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def second_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][1]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
    exchange = first_entity_value(entities, 'exchange')
    money = first_entity_value(entities, 'Money')
    money2 = second_entity_value(entities, 'Money')
    number = first_entity_value(entities, 'number')
    greeting = first_entity_value(entities, 'Greeting')
    bad = first_entity_value(entities, 'bad')
    if exchange:
        context['exchange'] = exchange
    if money:
        context['want']= money
    if money2:
        context['dest']=money2
    if number:
        context['number'] = number
    if greeting:
        context['greeting']=greeting
    if bad:
        context['badlanguage']=bad
    return context


def getcurrency(html):
    r = requests.get(html)
    element=web.Element(r.content)
    result = element('pod[title=result] subpod plaintext')[0].content
    return result


def error(session_id, context, e):
    print(str(e))

def getmoney(session_id, context):

    url='http://api.wolframalpha.com/v2/query?input='+str(context['number'])+context['want']+'+to+'+context['dest']+'&appid=G8U6WK-4W5YYQLK72'
    temp=getcurrency(url)
    context['realnumber']=temp
    return context



actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'getmoney': getmoney,
}

client = Wit(access_token, actions)
client.interactive()
