/*
The code for the beginTimer() function was written by Phil Schatzmann and can be found at the following link: https://www.pschatzmann.ch/home/2023/07/01/under-the-hood-arduino-uno-r4-timers/
All other functions and code in this file were written by Ben Thomas for use in this project, and are licensed under the MIT licesnse included with this git repository.
*/

#include "FspTimer.h"
#include <ArduinoBLE.h>

// --Timer varaibles--
FspTimer audio_timer;
uint64_t count=0;
uint64_t start_time=0;

// --Synth variables--
const float FREQ[4] = {261.63 * 16, 293.66 * 16, 329.63 * 16, 349.23 * 16};
const int BUZZER= A0;
const int SAMPLES[16] = {255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0};
int index = 0;
int gate = 1;

// --BLE Variables--
// Create service
BLEService myService("2c3a85a4-d811-49bf-91db-200cefb3ee3e");
// Create characteristic to transfer samples
BLECharacteristic sampleCharacteristic("192b2f69-868c-4a3c-b3c0-23cc991dbe82", BLERead | BLEWrite, 0xFF, 16);
// Advertising data (manufacturing data is set to the first 2 bytes of the UUID)
const uint8_t completeRawAdvertisingData[] = {0x02,0x01,0x06,0x09,0xff,0x2c,0x3a,0x85,0xa4,0xd8,0x11,0x49,0xbf};

// callback method used by timer
void timer_callback(timer_callback_args_t __attribute((unused)) *p_args) {
  if (gate == 0) {
    analogWrite(BUZZER, SAMPLES[index]);
  }
  index++;
  if (index == 16) {index = 0;}
}

bool beginTimer(float rate) {
  uint8_t timer_type = GPT_TIMER;
  int8_t tindex = FspTimer::get_available_timer(timer_type);
  if (tindex < 0){
    tindex = FspTimer::get_available_timer(timer_type, true);
  }
  if (tindex < 0){
    return false;
  }

  FspTimer::force_use_of_pwm_reserved_timer();

  if(!audio_timer.begin(TIMER_MODE_PERIODIC, timer_type, tindex, rate, 0.0f, timer_callback)){
    return false;
  }

  if (!audio_timer.setup_overflow_irq()){
    return false;
  }

  if (!audio_timer.open()){
    return false;
  }

  if (!audio_timer.start()){
    return false;
  }
  return true;
}

void setup() {
  Serial.begin(115200);

  // --BLE Initialization--
  if (!BLE.begin()) {
    Serial.println("failed to initialize BLE!");
    while (1);
  }
  // Advertising info
  BLE.setLocalName("Arduino Synth");
  BLE.setAdvertisedService(myService);

  // Add characteristics to service
  myService.addCharacteristic(sampleCharacteristic);

  // Add service to BLE
  BLE.addService(myService);

  // Initialize characteristics
  byte buffer[16] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0};
  sampleCharacteristic.writeValue(buffer, sizeof(buffer));

  BLE.advertise();
  Serial.println("advertising ...");

  // -- Synth initialization--
  // Initialize digital pins 0 through 3 for buttons
  // for (int i=0; i<4; i++) {
  //   pinMode(i, INPUT_PULLUP);
  // }
  pinMode(0, INPUT_PULLUP);
  pinMode(1, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(BUZZER, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  // beginTimer(6400);
  beginTimer(10);
}

void loop() {
  BLE.poll();

  int set = 1;
  // for (int i=0; i<4; i++) {
  //   if (digitalRead(i) == 0) {
  //     if (gate == 1) {
  //       audio_timer.set_frequency(FREQ[i]);
  //     }
  //     set = 0;
  //   }
  // }
  if (digitalRead(0) == 0) {
    if (gate) {
      audio_timer.set_frequency(FREQ[0]);
    }
    set = 0;
  }
  else if (digitalRead(1) == 0) {
    if (gate) {
      audio_timer.set_frequency(FREQ[1]);
    }
    set = 0;
  }
  else if (digitalRead(2) == 0) {
    if (gate) {
      audio_timer.set_frequency(FREQ[2]);
    }
    set = 0;
  }
  else if (digitalRead(3) == 0) {
    if (gate) {
      audio_timer.set_frequency(FREQ[3]);
    }
    set = 0;
  }
  gate = set;
  delay(100);
}
