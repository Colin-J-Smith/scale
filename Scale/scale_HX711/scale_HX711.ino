
#include <HX711.h>
#define DOUT 3
#define CLK 2
#define NUMSAMPLES 2
#define calibration_factor 1.0

HX711 scale;


int samples[NUMSAMPLES];
uint8_t i;
float sample_sum = 0;
float sample_avg = 1;

void setup() {
 Serial.begin(9600);
// Serial1.begin(9600);
 scale.begin(DOUT,CLK);
 scale.tare();  //Reset the scale to 0
 scale.set_scale(calibration_factor); //Adjust to this calibration factor
 delay(2500);
}


void loop() {
  
   // take N samples in a row, with a slight delay
  for (i = 0; i < NUMSAMPLES; i++) {
    samples[i] = scale.get_units();
    delay(2);
  }

  // Get the average of the last NUMSAMPLES
  sample_sum = 0;
  for (i = 0; i < NUMSAMPLES; i++) {
    sample_sum += samples[i];
  }
  sample_avg = sample_sum/NUMSAMPLES; //Value in lbs

  Serial.println(sample_avg);
//  Serial1.println(sample_avg);

}
