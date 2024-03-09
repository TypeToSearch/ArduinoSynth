/*
The code for the beginTimer() function was written by Phil Schatzmann and can be found at the following link: https://www.pschatzmann.ch/home/2023/07/01/under-the-hood-arduino-uno-r4-timers/
All other functions and code in this file were written by Ben Thomas for use in this project, and are licensed under the MIT licesnse included with this git repository.
*/

#include "FspTimer.h"

// Timer varaibles
FspTimer audio_timer;
uint64_t count=0;
uint64_t start_time=0;

// Synth variables
const int BUTTON = 13;
const int BUZZER = A0;
const int SAMPLES[16] = {127, 176, 217, 245, 255, 245, 217, 176, 127, 78, 37, 9, 0, 9, 37, 78};
int index = 0;
int gate = 0;

// callback method used by timer
void timer_callback(timer_callback_args_t __attribute((unused)) *p_args) {
  analogWrite(BUZZER, SAMPLES[index]);
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

  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(BUZZER, OUTPUT);
  pinMode(A5, INPUT);

  beginTimer(3200);
}

void loop() {
  delay(100);
}
