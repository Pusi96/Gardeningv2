int sensorpin1 = A0;
int sensorpin2 = A1;
int sensorValue1;
int sensorValue2;

int pump1 = 7;
int pump2 = 8;

int nedves = 400;
int szaraz = 820;
int threshold = 95;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pump1, OUTPUT);
  pinMode(pump2, OUTPUT);
  
}

void loop() {
  
  sensorValue1 = analogRead(sensorpin1);
  sensorValue2 = analogRead(sensorpin2);
  
  int szarazsag1 = map(sensorValue1, nedves, szaraz, 0, 100);
  int szarazsag2 = map(sensorValue2, nedves, szaraz, 0, 100);
  
  char toggle = Serial.read();
  
  Serial.print(szarazsag1);
  Serial.print(",");
  Serial.print(szarazsag2);
  Serial.println("");

  if (szarazsag1 > threshold || toggle == 'v') //if the soil is try then pump out water for 1 second
   {
   digitalWrite(pump1, LOW);
   delay(1000);
   digitalWrite(pump1, HIGH);
   }
   else if (szarazsag2 > threshold || toggle == 'f')
      {
   digitalWrite(pump2, LOW);
   delay(1000);  //run pump for 1 second;
   digitalWrite(pump2, HIGH);
   }
   else
   {
   digitalWrite(pump1, HIGH);
   digitalWrite(pump2, HIGH);
   }
   delay(1800000); //30 min
   //delay(80000);
   //delay(75000);
}
