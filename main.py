wifi_ssid = 'tatajewel'
wifi_pass = 'mimosa2020'
mqtt = None
mqtt_client = None
mqtt_server = b'mqtt.flespi.io'
mqtt_port = 1883
mqtt_user = b"8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE"
mqtt_pass = b''
mqtt_client_id = ubinascii.hexlify(machine.unique_id())
mqtt_topic_sub = b'microworking/telegram-iot/microthingv1/broker'
mqtt_topic_pub = b'microworking/telegram-iot/microthingv1/cloud'
mqtt_ssl = False
mqtt_counter = 0
mqtt_last_message = 0
mqtt_keepalive = 4000
mqtt_message_interval = 5
flow_control = 0
health_verify_cycle = 30000
process_verify_cycle = 2000
sensor = Pin(0, Pin.OUT, value=1)
buzzer = Pin(2, Pin.OUT, Pin.PULL_UP)
debug_mode = True
broadcast_enable = True
last_date_time = Helper.format_date_time(utime.time())
gpio0_state_0_read_message = 'O dispositivo %s esta ligado'    
gpio0_state_1_read_message = 'O dispositivo %s esta desligado'
gpio0_state_0_action_message = 'O dispositivo %s foi acionado pelo usuario %s'
gpio0_state_1_action_message = 'O dispositivo %s foi desligado pelo usuario %s'
no_peripheral_message = 'Ola %s, o dispositivo %s nao possui perifericos para controlar'
restart_message = 'O dispositivo %s sera reiniciado pelo usuario %s...por favor aguarde'
test_message = 'Ola %s, %s diz: beeeep! ;-)'
debug_mode_message = 'Debug mode %s para o dispositivo %s pelo usuario %s'
sound_enable_message = 'Som %s para o dispositivo %s pelo usuario %s'
broadcast_enable_message = 'Broadcast %s para o dispositivo %s pelo usuario %s'
action = ActionResponse()
action.identity_token = '8o1nx9zfTFUiAkYdgWR3GUlX9fxpREFOQw1dtoidR0jfa5ihR0alIj9GmuV4YrIE'
action.uid = Helper.get_uid()
action.gpio = 0
action.action = 'broadcast'
action.owner = 'device ' + Helper.get_uid()
action.update_id = 0
action.chat_id = 0
action.message_id = 0
action.peripheral = Helper.get_uid()
action.date = '2000-01-01T00:00:00.0000000Z'

def initialize():
  global mqtt, mqtt_client, action, debug_mode
  try:
    if debug_mode: print('Inicializing device %s...' % (Helper.get_uid()))
    health_check_stop()
    HttpHandler.do_connect()
    mqtt = MqttService()
    mqtt_client = mqtt.connect_and_subscribe()
    if debug_mode:
      action.message = 'Inicializing device %s...' % (Helper.get_uid())
      mqtt.publish_handler(action)
    health_check_start()
  except Exception as exception:
    if debug_mode:
      health_check_stop()
      print('Exception thrown in initialize: ' + str(exception))
    else:
      time.sleep(10)
      machine.reset()

initialize()
try:
  while True:
    try:
      if sensor.value() == 0 and flow_control == 1:
        flow_control = 0
        #action.message = gpio0_state_0_read_message % (Helper.get_uid())
        #if broadcast_enable: mqtt.publish_handler(action)
        if debug_mode: print('State value for GPIO 0 is 0')
      if sensor.value() == 1 and flow_control == 0:
        flow_control = 1
        #action.message = gpio0_state_1_read_message % (Helper.get_uid())
        #if broadcast_enable: mqtt.publish_handler(action)
        if debug_mode: print('State value for GPIO 0 is 1')
      mqtt_client.check_msg()
    except Exception as exception:
      if debug_mode:
        print('Exception thrown in main loop: ' + str(exception))
      else:
        time.sleep(10)
        initialize()
except Exception as exception:
  if debug_mode:
    print('Exception thrown in main flow: ' + str(exception))
  else:
    time.sleep(10)
    machine.reset()
