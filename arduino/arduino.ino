/*
The code for the beginTimer() function was written by Phil Schatzmann and can be found at the following link: https://www.pschatzmann.ch/home/2023/07/01/under-the-hood-arduino-uno-r4-timers/
All other functions and code in this file were written by Ben Thomas for use in this project, and are licensed under the MIT licesnse included with this git repository.
*/

#include "FspTimer.h"

FspTimer audio_timer;
uint64_t count=0;
uint64_t start_time=0;

const int SAMPLES[] = {};

// callback method used by timer
void timer_callback(timer_callback_args_t __attribute((unused)) *p_args) {
  count++;
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
  beginTimer(40000);
  start_time = millis();
}

void loop() {
  // calculate the effective frequency
  int freq = 1000 * count / (millis()-start_time);
  Serial.println(freq);
  count = 0;
  start_time = millis();
  delay(1000);
}
