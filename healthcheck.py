health_timer = Timer(-1)

def health_check_start():
  global health_timer, health_verify_cycle
  health_timer = Timer(-1)
  health_timer.init(period=health_verify_cycle, mode=Timer.PERIODIC, callback=lambda t:check())
  
def health_check_stop():
  global health_timer
  health_timer.deinit()
  
def check():
  health_check_stop()
  #http_check() #HTTP check is disable 
  mqtt_check()
  health_check_start()

def mqtt_check():
    global mqtt, debug_mode, last_date_time
    uid = Helper.get_uid()
    action = ActionResponse()
    action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
    action.uid = uid
    action.gpio = 0
    action.action = 'ping'
    action.owner = 'device %s' % (uid)
    action.update_id = 0
    action.chat_id = 0
    action.message_id = 0
    action.peripheral = uid
    action.message = 'Device %s MQTT health checking' % (uid)
    action.date = last_date_time
    mqtt.publish_handler(action)
    if debug_mode: print('Verifying MQTT health...')

def http_check():
    global debug_mode
    if debug_mode: print('Verifying network health...')
    sta_if = network.WLAN(network.STA_IF)
    if(not sta_if.isconnected() or not HttpHandler.http_get('http://www.google.com/', 80)):
      if debug_mode: print('Network disconected! Reconecting...')
      initialize()
    else:
      if debug_mode: print('HTTP healthing!')


