/*improvement: 
 * 
 * Use microsencods() instead of millis() to prevent timestamp values duplicates.
 */

#define BWPress A0 //bladder/water
#define LED1 13//2 //status data collection via LED1. If continuously on, data is being collected or is ready to collect data. If blinking, collection is terminated.

float pressure = 0.0;
float minpressure = 3.0; // minpressure to be printed. Previously 0.22
int flag=0;
float hold = 0;
unsigned long lastprixnt=0;//
int puffNumber=1;
int outputcounter=1;
int count = 1;
void setup() {
  Serial.begin(115200);
  pinMode(LED1, OUTPUT);
  pinMode(BWPress, INPUT);
  digitalWrite(LED1, LOW);

int state=0;
String mes;
  while(state==0){
    if (Serial.available()>0){
    mes = Serial.readStringUntil('\n');
    if (mes == "W"){
      digitalWrite(LED1, HIGH);
      Serial.print("A");
      state = 1;
    }
   }
  }
}
void loop(){
Pressureread();
}

void Pressureread() {
    
    pressure = analogRead(BWPress);  // reading pin BWPress pin (0-->1024)
    pressure=((pressure/1023.0)*5.0); // 0 to 5 V = outV
    pressure = ((pressure-0.5)*1.25); // pressure in psi ....Equation:   Output(V) = (0.8 x Vsupply/(Pmax-Pmin)) x (Pressureapplied – Pmin.) + (0.10 x Vsupply)
    pressure=constrain(pressure, 0.0, 5.0);
    
    if (pressure >= minpressure){ // signal conditioning
        
        pressure = analogRead(BWPress);  // reading pin BWPress pin (0-->1024)
        pressure=((pressure/1023.0)*5.0); // 0 to 5 V = outV
        pressure = ((pressure-0.5)*1.25); // pressure in psi ....Equation:   Output(V) = (0.8 x Vsupply/(Pmax-Pmin)) x (Pressureapplied – Pmin.) + (0.10 x Vsupply)
        pressure=constrain(pressure, 0.0, 5.0);
     
        Serial.print(millis()); //prints the current number of ms since code began running
        Serial.print(","); //adds comma delimiter
        Serial.println(pressure); //prints pressure value at current time
        count = 0; //continually makes counter 0 so that next if statement is false
    }

    // This section of code will check to see if pressure has just reached below the threshold
    // and will print out a label for the trial.
    else if (count == 0 && pressure<0.03){
    Serial.println("*" + String(outputcounter));
    count = 1;
    outputcounter = outputcounter + 1;
    
    if (outputcounter > 6){
    Serial.println("E");
    while(true){
      digitalWrite(LED1, HIGH);
      delay(1000);
      digitalWrite(LED1, LOW);
      delay(1000);
    }
    }
    }
}
//    }
//    /*
//    if((millis()-lastprint)>=1000 && flag==1){
//      flag=0;
//      Counter=0;
//      Serial.print("*");
//      //Serial.print(puffNumber);
//      //Serial.println("*");
//      puffNumber=puffNumber+1;
//      
//    }
//    */
//    
////    if (puffNumber==11){
////      puffNumber=1;
////    }
//    
////    Tpressure=analogRead(TankPress);
////    Tpressure=((Tpressure/1023.0)*5.0);
////    Tpressure=((Tpressure-0.5)*7.5);
////    Tpressure=constrain(Tpressure, 0.0, 30.0);
//
//    // comment this for production firmware
//    //Serial.print("Tank sensor pressure  ");
//    //Serial.println(Tpressure);
//    //Serial.println("");
////    
////    Serial.print("bin pressure  ");
////    Serial.println(analogRead(TankPress));
//}
