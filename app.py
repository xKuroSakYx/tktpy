from flask import Flask, request, redirect, session, send_file, make_response
from flask_cors import CORS
from telethon.errors.rpcerrorlist import PeerFloodError
import os
import asyncio
#import psycopg2
import mysql.connector
import time
import csv

from config.config import startConnection, startConnection2, validateUsername, validUserFromDb, config, calculate_sha256, storeTwitter, validateTwitterTelegram, validateWallet, authCode, timestamp, storeCode, getStoreCode, validateTwitter, getWallets, getReferidos

######################## TWITTER OAUTH ######################
from requests_oauthlib import OAuth1Session
import json
import requests
#############################################################

_TOKEN_ = 'tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s'
_TOKEN_ADMIN_ = 'tktktsSyMgZv8caqyg9wtsSyMgZv8caqygGGhtsStsSyMgZv8caqygyMgZv8caqygNgPVMrdDw02IZlnRhbK3sMrdDw02IZlnRhbK3s'
_USERADMIN_ = "Eric"
_TIMEMAX_ = 600
_TIMEMIN_ = 90
######################## TWITTER OAUTH ######################
consumer_key='Gi22eaK49RxNH9uYhJquV0v4u'
consumer_secret= 'rQJKpa4p8j8Pc1Ju9llERSDyCcj6NuKwyXrGJy4wHFYcDIU923'

#web_url = "http://localhost:8080"
web_url = "https://airdrop.x6nge.io/"
request_token_url = "https://api.twitter.com/oauth/request_token"
access_token_url = "https://api.twitter.com/oauth/access_token"

fields = "created_at,description"
params = {"user.fields": fields}

#############################################################

# http://127.0.0.1:5000/api/telegram?token=tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s&user=kalguanchez&group=thekeyoftrueTKT&type=broadcast
# http://127.0.0.1:5000/api/telegram?token=tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s&user=Davier&group=thekeyoftrueTKT&type=broadcast
# http://127.0.0.1:5000/api/cleandb?token=tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s
# http://127.0.0.1:5000/api/updatebd?token=tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s&user=5900098531
# postgres://telegrambot_tkt_user:7p2uqGFWiPARqzIyEsOcsqRv00C0g50e@dpg-ck68gl5drqvc73bj9kpg-a.oregon-postgres.render.com/telegrambot_tkt
# gunicorn --bind 0.0.0.0:8000 app:app


app = Flask(__name__, instance_relative_config=False)
app.secret_key = os.urandom(50)
#CORS(app, supports_credentials=True)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

######################## TWITTER OAUTH ######################
@app.route("/authcode", methods=["GET"])
async def authcode():
    client = await startConnection()
    client2 = await startConnection2()
    await client.disconnect()
    await client2.disconnect()
    return app.response_class(
        response=json.dumps({'response': 'client ok'}),
        status=200,
        mimetype='application/json'
    ) 

#http://127.0.0.1:5000/twitter?token=tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s&username=DarkRaimbos&id=1702685702037577731
@app.route("/twitter", methods=["GET"])
def twitter():
    token = request.args.get('token')
    mId = request.args.get('id')
    mUsername = request.args.get('username')

    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    validTwitter = validateTwitter(mId, mUsername)
    print('Validater twitter ban es %s'% validTwitter['twitterban'])
    if(validTwitter is not None and validTwitter['twitterban']):
        return app.response_class(
            response=json.dumps({
                'username': mUsername,
                'error': 'user_twitter_banned',
                'twitteralert': True
            }),
            status=200,
            mimetype='application/json'
        )
    if(validTwitter is not None and validTwitter['twitterexist']):
        if(not validTwitter['twittervalid']):
            return app.response_class(
                response=json.dumps({
                    'username': mUsername,
                    'error': 'user_twitter_exist',
                    'twitteralert': True
                }),
                status=200,
                mimetype='application/json'
            )
            return redirect('%s/?twitteralert=true&error=user_twitter_exist&username=%s'%(web_url, mUsername))
    print("llego aquiiiiiiiiiiiiiiiiiii") 
    #http://localhost:5001/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username=lii_mmminseon5
    try:
        if(session[mUsername] == 4):
            session[mUsername] = 0
        else:
            session[mUsername] = session[mUsername] + 1
    except:
        session[mUsername] = 0
    
    spaces = session[mUsername]
    print('los spacios son %sf'%spaces)
    ind = 0
    while 1:
        #print("se hizo break por 10 %s" % ind)
        if(ind == 3):
            #print("se hizo break por 10")
            break
        try:
            if(not session['5001']):
                session['5001'] = True
                #print("se envio la peticion")
                try:
                    resp = requests.get('http://localhost:5001/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(mUsername, spaces), timeout=25)

                except:
                    print(resp.text)
                    print("el error es la peticion")
                session['5001'] = False
                print('session 5001 es %s' % session['5001'])
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5001 dio error")
            session['5001'] = False

        try:
            if(not session['5002']):
                session['5002'] = True
                resp = requests.get('http://localhost:5002/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(mUsername, spaces), timeout=25)
                session['5002'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5002 dio error")
            session['5002'] = False

        try:
            if(not session['5003']):
                session['5003'] = True
                resp = requests.get('http://localhost:5003/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(mUsername, spaces), timeout=25)
                session['5003'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5003 dio error")
            session['5003'] = False

        try:
            if(not session['5004']):
                session['5004'] = True
                resp = requests.get('http://localhost:5004/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(mUsername, spaces), timeout=25)
                session['5004'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5004 dio error")
            session['5004'] = False

        try:
            if(not session['5005']):
                session['5005'] = True
                resp = requests.get('http://localhost:5005/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(mUsername, spaces), timeout=25)
                session['5005'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5005 dio error")
            session['5005'] = False

        ind+=1
        print("reintento %s de conexion " % ind)
    if(ind >= 3):
        return app.response_class(
            response=json.dumps({
                'username': mUsername,
                'error': 'connexion_timeout',
                'twitteralert': True
            }),
            status=200,
            mimetype='application/json'
        )
        #return redirect('%s/?twitteralert=true&error=connexion_timeout'%(web_url))

    jresponse = resp.json()
    isfollow = jresponse['response']
    print(jresponse)

    if(isfollow == 'username_follows'):
        mFollow = 'valid'
    elif(isfollow == 'username_not_follow'):
        mFollow = 'invalid'
    elif(isfollow == 'username_not_exist'):
        mFollow = 'notexist'

    hash_value = calculate_sha256('%s' % mId)

    stwitter = storeTwitter(mId, mUsername, mFollow, hash_value)
    if(stwitter):
        return app.response_class(
            response=json.dumps({
                'username': mUsername,
                'twitter': mFollow,
                'hash': hash_value,
                'twitteralert': True,
                'error': 'false'
            }),
            status=200,
            mimetype='application/json'
        ) 
        #return redirect('%s/?username=%s&twitter=%s&hash=%s&twitteralert=true'%(web_url, mUsername, mFollow, hash_value))
    else:
        return app.response_class(
            response=json.dumps({
                'username': mUsername,
                'error': 'not_stored_twitter_user',
                'twitteralert': True
            }),
            status=200,
            mimetype='application/json'
        )
        #return redirect('%s/?twitteralert=true&error=not_stored_twitter_user&username=%s'%(web_url, mUsername))
    #print(json.dumps(json_response, indent=4, sort_keys=True))

@app.route("/", methods=["GET"])
def index():
    #session['8000'] = False
    #session['8001'] = False
    #session['8002'] = False
    #session['8003'] = False
    #session['8004'] = False
    #session['8005'] = False
    
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    #request.cookies
    #request.cookies.add('resource_owner_key', resource_owner_key)
    #request.cookies.add('resource_owner_secret', resource_owner_secret)

    #session['ip'] = {'resource_owner_key': resource_owner_key, "resource_owner_secret": resource_owner_secret}
    
    #session["%s1"%ip] = resource_owner_key
    #session["%s2"%ip]  = resource_owner_secret

    # # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    
    resp = make_response(redirect(authorization_url))
    resp.set_cookie('resource_owner_key', resource_owner_key)
    resp.set_cookie('resource_owner_secret', resource_owner_secret)

    """
        myResponse = make_response('Response')
        myResponse.headers['customHeader'] = 'This is a custom header'
        myResponse.status_code = 403
        myResponse.mimetype = 'video/mp4'
    """
    return resp

@app.route("/oauth/callback", methods=["GET"])
def callback():
    try:
        resource_owner_key = request.cookies.get('resource_owner_key')
        resource_owner_secret = request.cookies.get('resource_owner_secret')
    except:
        return redirect('%s/?twitteralert=true&error=connexion_timeout'%(web_url))

    verifier = request.args.get("oauth_verifier")
    print("el toen de verificacion %s"%verifier)
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    try:
        oauth_tokens = oauth.fetch_access_token(access_token_url)
    except:
        print("error token request denied")
        return redirect('%s/?twitteralert=true&error=connexion_timeout'%(web_url))
    
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.get("https://api.twitter.com/2/users/me", params=params)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    json_response = response.json()
    print(json_response)

    mId = json_response['data']['id']
    mUsername = json_response['data']['username']
    
    validTwitter = validateTwitter(mId, mUsername)
    if(validTwitter is not None and validTwitter['twitterexist']):
        if(not validTwitter['twittervalid']):
            return redirect('%s/?twitteralert=true&error=user_twitter_exist&username=%s'%(web_url, mUsername))
        
    #http://localhost:5001/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username=lii_mmminseon5
    try:
        if(session[mUsername] == 4):
            session[mUsername] = 0
        else:
            session[mUsername] = session[mUsername] + 1
    except:
        session[mUsername] = 0
    
    spaces = session[mUsername]
    ind = 0
    while 1:
        #print("se hizo break por 10 %s" % ind)
        if(ind == 3):
            #print("se hizo break por 10")
            break
        try:
            if(not session['5001']):
                session['5001'] = True
                #print("se envio la peticion")
                resp = requests.get('http://localhost:5001/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(json_response['data']['username'], spaces), timeout=25)
                session['5001'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5001 dio error")
            session['5001'] = False

        try:
            if(not session['5002']):
                session['5002'] = True
                resp = requests.get('http://localhost:5002/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(json_response['data']['username'], spaces), timeout=25)
                session['5002'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5002 dio error")
            session['5002'] = False

        try:
            if(not session['5003']):
                session['5003'] = True
                resp = requests.get('http://localhost:5003/auth?token=tktk9wv7I8UU26FGGhtsSyMgZvmco8caqygNgPVMrdDw02IZlnRhbK3s&username={}&spaces={}'.format(json_response['data']['username'], spaces), timeout=25)
                session['5003'] = False
                if resp.status_code != 200:
                    print(resp.text)
                else:
                    if(resp.json()['response'] == 'error_in_validuser'):
                        pass
                    else:
                        break
        except:
            print("sessiom 5003 dio error")
            session['5003'] = False
        
        ind+=1
        print("reintento %s de conexion " % ind)
    if(ind >= 3):
        return redirect('%s/?twitteralert=true&error=connexion_timeout'%(web_url))

    jresponse = resp.json()
    isfollow = jresponse['response']
    print(jresponse)

    if(isfollow == 'username_follows'):
        mFollow = 'valid'
    elif(isfollow == 'username_not_follow'):
        mFollow = 'invalid'
    elif(isfollow == 'username_not_exist'):
        mFollow = 'notexist'

    hash_value = calculate_sha256('%s' % mId)

    stwitter = storeTwitter(mId, mUsername, mFollow, hash_value)
    if(stwitter):
        return redirect('%s/?username=%s&twitter=%s&hash=%s&twitteralert=true'%(web_url, mUsername, mFollow, hash_value))
    else:
        return redirect('%s/?twitteralert=true&error=not_stored_twitter_user&username=%s'%(web_url, mUsername))
    #print(json.dumps(json_response, indent=4, sort_keys=True))

#############################################################

@app.route('/api/telegram', methods=["GET"])
async def telegramget():
    token = request.args.get('token')
    user = request.args.get('username')
    try:
        if(valid['response'] != "user_banned"):
            hash = request.args.get('hash')
            id = request.args.get('id')

            ######################
            timeactual = timestamp()
            valid = validUserFromDb(user)
            
            scode = getStoreCode(id, hash)
            #print("el sms guardado es %s" % scode[0])
            returndata = ""

            timedif = scode[1] - timeactual
            if(timedif <= _TIMEMAX_):
                hash_value = calculate_sha256("%s" % id)
                returndata = {'response': 'user_ok_re', 'hash': hash_value, 'id': id}
            else:
                returndata = {'response': 'code_error_time'}
            
            response = app.response_class(
                response=json.dumps(returndata),
                status=200,
                mimetype='application/json'
            )
            return response

            ######################
    except:
        pass
    #print(token+" "+user+" "+group+" "+type)
    returndata = ""

    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    ind = 0
    while 1:
        try:
            client = await startConnection2()
            break
        except:
            time.sleep(0.3)
            ind+=1
        if ind == 100:
            client = await startConnection()
            break
    
    if ind >= 100:
        return app.response_class(
            response=json.dumps({'response': 'user_error'}),
            status=200,
            mimetype='application/json'
        )
    try:
        valid = validUserFromDb(user)
        print("%s and user %s" % (valid['response'], user))
        if(valid['response'] == "user_banned"):
            returndata = {'response': 'user_telegram_banned'}
        elif(valid['response'] == "user_ok"):
            
            hash_value = calculate_sha256("%s" % valid['userid'])
            smscode = authCode()
            message = "Hello @{}, The Key of True telegram user verification code: %s." % smscode
            store = storeCode(valid['userid'], smscode, timestamp(), _TIMEMIN_)

            if(store["response"] == "store_code_ok"):
                try:
                    receiver = await client.get_input_entity(user.replace("@", ""))
                    await client.send_message(receiver, message.format(user))
                except PeerFloodError:
                    pass
                    #print("[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
                except Exception as e:
                    pass
                    #print("[!] Error:", e)
                    #print("[!] Trying to continue...")
                returndata = {'response': 'user_ok', 'hash': hash_value, 'id': valid['userid']}
            elif(store["response"] == "store_code_timeout"):
                returndata = {'response': 'user_timeout', 'segundos': _TIMEMIN_ - store['segundos']}
                print("los segundos de menos son %s "%store['segundos'])
            else:
                print("los segundos de menos son %s "% _TIMEMIN_)
                returndata = {'response': 'user_timeout', 'segundos': _TIMEMIN_}

        elif valid['response'] == "user_exist":
            returndata = {'response': 'user_exist'}
        elif(valid['response'] == "user_not_registry"):
            try:
                message = 'Hello @{}, you need to join the telegram channel https://t.me/thekeyoftrueTKT, if you are already a subscriber, join the group and then verify your username again in the airdrop. Thank you for your support.'
                receiver = await client.get_input_entity(user.replace("@", ""))
                await client.send_message(receiver, message.format(user))
            except PeerFloodError:
                pass
                #print("[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
            except Exception as e:
                pass
            returndata = {'response': "user_not_registry"}
        elif valid['response'] == "user_error":
            returndata = {'response': 'user_error'}

        await client.disconnect()

        response = app.response_class(
            response=json.dumps(returndata),
            status=200,
            mimetype='application/json'
        )
        return response
    except:
        return app.response_class(
            response=json.dumps({'response': 'user_timeout'}),
            status=200,
            mimetype='application/json'
        )

@app.route('/api/telegram', methods=["POST"])
async def telegram():
    data = request.get_json()
    user = data["username"]
    user = user.replace("@", "")
    token = data["token"]
    #group = data["group"]
    #type = data["type"]
    returndata = ""
    client = None 
    #print(token+" "+user+" "+group+" "+type)
    #time.sleep(4)
    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    ind = 0
    while 1:
        try:
            client = await startConnection()
            break
        except:
            time.sleep(0.3)
            ind+=1
        if ind == 100:
            break
    
    if ind >= 100:
        return app.response_class(
            response=json.dumps({'response': 'user_error'}),
            status=200,
            mimetype='application/json'
        )
    
    valid = validUserFromDb(user)
    
    if(valid['response'] == "user_ok"):
        
        hash_value = calculate_sha256("%s" % valid['userid'])
        message = authCode()
        store = storeCode(valid['userid'], message, timestamp(), _TIMEMIN_)
        
        if(store["response"] == "store_code_ok"):
            try:
                receiver = await client.get_input_entity(user)
                await client.send_message(receiver, message.format(user))
            except PeerFloodError:
                pass
                #print("[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
            except Exception as e:
                pass
                #print("[!] Error:", e)
                #print("[!] Trying to continue...")
            returndata = {'response': 'user_ok', 'hash': hash_value, 'id': valid['userid']}
        elif(store["response"] == "store_code_timeout"):
            returndata = {'response': 'user_timeout', 'segundos': store['segundos']}
            print("los segundos de menos son %s "%store['segundos'])
        else:
            print("los segundos de menos son %s "% _TIMEMIN_)
            returndata = {'response': 'user_timeout', 'segundos': _TIMEMIN_}

    elif valid['response'] == "user_exist":
        returndata = {'response': 'user_exist'}
    elif(valid['response'] == "user_not_registry"):
        returndata = {'response': "user_not_registry"}
    elif valid['response'] == "user_error":
        returndata = {'response': 'user_error'}

    await client.disconnect()
    print("el return data")
    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/telegram/code', methods=["GET"])
async def telegramCodeGet():
    token = request.args.get('token')
    hash = request.args.get('hash')
    id = request.args.get('id')
    code = request.args.get('code')
    
    #time.sleep(4)
    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    timeactual = timestamp()
    
    scode = getStoreCode(id, hash)
    print("el sms guardado es %s" % scode[0])
    returndata = ""

    timedif = scode[1] - timeactual
    print("print el timedef es %s el code %s el storecode %s el tim %s " % (timedif, code, scode[0], scode[1]))
    if(timedif <= _TIMEMAX_):
        if(int(code) == int(scode[0])):
            returndata = {'response': 'code_ok'}
        else:
            returndata = {'response': 'code_error'}
    else:
        returndata = {'response': 'code_error_time'}
    

    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/telegram/code', methods=["POST"])
async def telegramCode():
    data = request.get_json()
    token = data["token"]
    hash = data["hash"]
    id = data["id"]
    code = data["code"]
    
    #time.sleep(4)
    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    timeactual = timestamp()
    
    scode = getStoreCode(id, hash)
    print("el sms guardado es %s" % scode[0])
    returndata = ""

    timedif = scode[1] - timeactual
    print("print el timedef es %s el code %s el storecode %s el tim %s " % (timedif, code, scode[0], scode[1]))
    if(timedif <= _TIMEMAX_):
        if(int(code) == int(scode[0])):
            returndata = {'response': 'code_ok'}
        else:
            returndata = {'response': 'code_error'}
    else:
        returndata = {'response': 'code_error_time'}
    

    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/cleandb', methods=["GET"])
def cleandb():
    token = request.args.get('token')

    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    returndata = ""

    try:
        conexion = None
        params = config()
        #print(params)

        # Conexion al servidor de MySql
        print('Conectando a la base de datos MySql...')
        conexion = mysql.connector.connect(**params)
        
        # creación del cursor
        cur = conexion.cursor()
        cur.execute("DROP TABLE IF EXISTS telegram")
        conexion.commit()
        print("se elimino la tabla correctamente")
        conexion.close()
        returndata = {'response': 'clean_bd_ok'}
    except (Exception) as error:
        print(error)
        returndata = {'response': 'clean_bd_ok', 'data': error}
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/updatebd', methods=["GET"])
def updatebd():
    token = request.args.get('token')
    user = request.args.get('user')
    value = request.args.get('value')
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    if(user == None or user == ""):
        return app.response_class(
            response=json.dumps({'response': 'invalid User'}),
            status=200,
            mimetype='application/json'
        )
    
    if(value == None):
        value = 1

    returndata = ""

    try:
        conexion = None
        params = config()
        #print(params)

        # Conexion al servidor de MySql
        print('Conectando a la base de datos MySql...')
        conexion = mysql.connector.connect(**params)
        
        # creación del cursor
        cur = conexion.cursor()
        sql = "UPDATE telegram SET valid=%s WHERE userid=%s;"
        cur.execute(sql, (value, user))
        print("actualizando la base de datos")
        conexion.commit()
        cur.execute( "SELECT userid, valid FROM telegram" )

        # Recorremos los resultados y los mostramos

        userlist = cur.fetchall()
        for userid, valid in userlist :
            print("revisando la lista de los usuarios: %s valid: %s"%(userid, valid))
        # Cierre de la comunicación con MySql
        conexion.close()
        print("se cerro la conexion con la base de datos")
        returndata = {'response': 'user_updated_ok'}

    except (Exception) as error:
        print(error)
        returndata = {'response': 'user_updated_error', 'data': error}
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/getusers', methods=["GET"])
def getusers():
    token = request.args.get('token')
    user = request.args.get('user')
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    if(user == None or user == ""):
        return app.response_class(
            response=json.dumps({'response': 'invalid User'}),
            status=200,
            mimetype='application/json'
        )
    
    try:
        conexion = None
        params = config()
        print('Conectando a la base de datos MySql...')
        conexion = mysql.connector.connect(**params)
        
        cur = conexion.cursor()
        cur.execute( "SELECT userid, valid FROM telegram" )
        ListUser = []
        userlist = cur.fetchall()
        for userid, valid in userlist :
            ListUser.append([userid, valid])
            print("revisando la lista de los usuarios: %s valid: %s"%(userid, valid))
        conexion.close()
        print("se cerro la conexion con la base de datos")
        return {'response': 'user_list_ok', 'data': ListUser}

    except (Exception) as error:
        print(error)
        return {'response': 'user_updated_error', 'data': error}
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

####################AUTENTICATE WALLET##################
## http://127.0.0.1:5000/api/wallet?token=tktk9wv7I8UU26FGGhtsSyMgZv8caqygNgPVMrdDw02IZlnRhbK3s&wallet=marloncruzoo&twitter=9179fb55a5fb0fe8f0a7bdbd6c906bbad24cf63b5bd9e598d026342a27a888a7&telegram=9fcb1a4f53f245788d9cb5b0a51d0fac42630f600963193d734ac37cb5ae05da&referido=2018181c452f44e583195440a3d9e9cc8bd4f3a25809409089078b9d2871b3cc
@app.route('/api/wallet', methods=["GET"])
async def walletGet():
    token = request.args.get('token')
    wallet = request.args.get('wallet')
    twitter = request.args.get('twitter')
    telegram = request.args.get('telegram')
    referido = request.args.get('referido')

    print(" /api/wallet el enlace de referido es %s" % referido)
    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    returndata = ""

    val = validateTwitterTelegram(twitter, telegram)

    isok =False
    print('twitter van %s'% val['twitterban'])
    if(val is None):
        returndata = {'response': 'user_error_valid'}
    elif(val['twitterban']):
        returndata = {'response': 'user_twitter_banned'}
    elif(val['telegramban']):
        returndata = {'response': 'user_telegram_banned'}
    elif(val['twitterexist'] and val['telegramexist']):
        if(not val['twittervalid']):
            returndata = {'response': 'user_twitter_exist'}
        else:
            if(not val['telegramvalid'] ):
                returndata = {'response': 'user_telegram_exist'}
            else:
                isok = True
        
    elif(not val['twitterexist']):
        returndata = {'response': 'user_twitter_notexist'}

    elif(not val['telegramexist']):
        returndata = {'response': 'user_telegram_notexist'}

    if(isok):
        vWallet = validateWallet(wallet, referido, twitter, telegram, val['twittervalid'], val['telegramvalid'])
        if(vWallet[0] == 'banned'):
            returndata = {'response': 'user_wallet_banned'}
        elif(vWallet[0] == 'error'):
            returndata = {'response': vWallet[1]}
        elif(vWallet[0] == 'notpaid'):
            returndata = {'response': 'user_wallet_notpaid', "data": vWallet[1]}
        elif vWallet[0] == 'paid':
            returndata = {'response': 'user_wallet_paid', "data": vWallet[1]}
        elif vWallet[0] == 'ok':
            returndata = {'response': 'user_wallet_ok', "data": vWallet[1], "reflink": vWallet[2]}

    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/wallet', methods=["POST"])
async def wallet():
    data = request.get_json()
    token = data["token"]
    wallet = data["wallet"]
    twitter = data["twitter"]
    telegram = data["telegram"]
    referido = data["referido"]

    print(" /api/wallet el enlace de referido es %s" % referido)
    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    returndata = ""

    val = validateTwitterTelegram(twitter, telegram)

    isok =False
    if(val is not None and val['twitterexist'] and val['telegramexist']):
        if(not val['twittervalid']):
            returndata = {'response': 'user_twitter_exist'}
        else:
            if(not val['telegramvalid'] ):
                returndata = {'response': 'user_telegram_exist'}
            else:
                isok = True
        
    elif(not val['twitterexist']):
        returndata = {'response': 'user_twitter_notexist'}

    elif(not val['telegramexist']):
        returndata = {'response': 'user_telegram_notexist'}

    if(isok):
        vWallet = validateWallet(wallet, referido)
        if(vWallet[0] == 'banned'):
            returndata = {'response': 'user_wallet_banned'}
        elif(vWallet[0] == 'error'):
            returndata = {'response': vWallet[1]}
        elif(vWallet[0] == 'notpaid'):
            returndata = {'response': 'user_wallet_notpaid', "data": vWallet[1]}
        elif vWallet[0] == 'paid':
            returndata = {'response': 'user_wallet_paid', "data": vWallet[1]}
        elif vWallet[0] == 'ok':
            returndata = {'response': 'user_wallet_ok', "data": vWallet[1], "reflink": vWallet[2]}

    response = app.response_class(
        response=json.dumps(returndata),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/api/getwallets', methods=["GET"])
async def getwallet():

    token = request.args.get('token')
    user = request.args.get('user')

    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ADMIN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    if(user != _USERADMIN_):
        return app.response_class(
            response=json.dumps({'response': 'invalid Username'}),
            status=200,
            mimetype='application/json'
        )
    
    csvWallet = getWallets(os.getcwd()+"/csv/")
    csvWallet = os.path.join(os.getcwd()+"/csv/", csvWallet)

    response = app.response_class(
        response=json.dumps({'response': 'No Se pudo Devolver el archivo intente de nuevo'}),
        status=200,
        mimetype='application/json'
    )
    print(csvWallet)
    if csvWallet:
        #file_path = os.path.join(os.getcwd()+"csv/", csvWallet)
        return send_file(csvWallet)
    else:
        return response

@app.route('/api/getpruwallets', methods=["GET"])
async def getPruwallet():

    token = request.args.get('token')
    user = request.args.get('user')

    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ADMIN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    
    if(user != _USERADMIN_):
        return app.response_class(
            response=json.dumps({'response': 'invalid Username'}),
            status=200,
            mimetype='application/json'
        )
    
    csvWallet = getWallets(os.getcwd()+"/csv/", True)
    csvWallet = os.path.join(os.getcwd()+"/csv/", csvWallet)

    response = app.response_class(
        response=json.dumps({'response': 'No Se pudo Devolver el archivo intente de nuevo'}),
        status=200,
        mimetype='application/json'
    )
    print(csvWallet)
    if csvWallet:
        #file_path = os.path.join(os.getcwd()+"csv/", csvWallet)
        return send_file(csvWallet)
    else:
        return response


@app.route('/api/getrefwallets', methods=["GET"])
async def getRefwallet():

    token = request.args.get('token')
    wallet = request.args.get('wallet')

    #return {'response': 'user_ok', 'data': "okok"}
    print("token %s %s"%(_TOKEN_, token))
    if(_TOKEN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    referidos = getReferidos(wallet)
    print(referidos['response'])
    try:
        if(referidos['response'] == 'ok'):
            response = app.response_class(
                response=json.dumps({'response': 'get_refdata_ok', 'ref_total': referidos['data'][0], 'ref_paid': referidos['data'][1], 'ref_id': referidos['data'][2]}),
                status=200,
                mimetype='application/json'
            )
        else:
            response = app.response_class(
                response=json.dumps({'response': 'get_refdata_error'}),
                status=200,
                mimetype='application/json'
            )
    except:
        response = app.response_class(
            response=json.dumps({'response': 'get_refdata_error'}),
            status=200,
            mimetype='application/json'
        )
    return response

@app.route('/api/getwalletscsv', methods=["GET"])
async def getwalletcsv():

    token = request.args.get('token')
    user = request.args.get('user')
    day = request.args.get('day')
    mes = request.args.get('mont')
    year = request.args.get('year')

    #return {'response': 'user_ok', 'data': "okok"}
    if(_TOKEN_ADMIN_ != token):
        return app.response_class(
            response=json.dumps({'response': 'invalid Token'}),
            status=200,
            mimetype='application/json'
        )
    if(user != _USERADMIN_):
        return app.response_class(
            response=json.dumps({'response': 'invalid Username'}),
            status=200,
            mimetype='application/json'
        )
    
    
    filename = os.path.join(os.getcwd()+"\csv", "wallets_%s_%s_%s.csv" % (day, mes, year))
    if(os.path.isfile(filename)):
         return send_file(filename)
    else:
        response = app.response_class(
            response=json.dumps({'response': 'No se pudo encontrar el archivo %s ' % filename}),
            status=200,
            mimetype='application/json'
        )
    return response
########################################################
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
