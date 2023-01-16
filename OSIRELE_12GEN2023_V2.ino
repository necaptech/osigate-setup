// Prodotta a partire da OSIRELE_22DIC2019_rev1
// per adattare al nuovo OsiGATE

//--------------------------------------------SETTAGGI------------------------------------------------
long randNumber ;
int randSleep ;
word randTX ;
int DELAY_BEE_ON = 100 ; // ritardo di stabilizzazione in millisecondi delle radio in accensione
int DELAY_BEE_OFF = 2000 ; // ritardo di stabilizzazione in millisecondi delle radio in spegnimento

const char ID_NODE_1  = 'R';
const char ID_NODE_2  = '0';
const char ID_NODE_3  = '0';
const char ID_NODE_4  = '0';
const char ID_NODE_5  = '2';
const char ID_NODE_6  = '7';

const byte SET_RADIO = A0 ; // set pin HIGH to enable radio 
const byte POWER_BEE = 5;   // set pin LOW to power ON radio

const byte CMD_RELE_1A =  8;   // set pin HIGH to enable relè              
const byte CMD_RELE_2A =  7;   // set pin HIGH to enable relè
const byte CMD_RELE_3B =  4;   // set pin HIGH to enable relè              
const byte CMD_RELE_4B =  3;   // set pin HIGH to enable relè
const byte CMD_RELE_5C =  2;   // set pin HIGH to enable relè              
const byte CMD_RELE_6C =  A3;   // set pin HIGH to enable relè
const byte CMD_RELE_7D =  A2;   // set pin HIGH to enable relè              
const byte CMD_RELE_8D =  A1;   // set pin HIGH to enable relè

const bool MostraStatus = false;  // mostra status pin ogni ciclo


//--------------SERIALE VIRTUALE ----------------------------------------------------------------------

#include <SoftwareSerial.h>
#define rxpin 6
#define txpin 13
const int Seriale_Radio = 1200 ;   // velocità della seriale radio
SoftwareSerial BEE_Serial(rxpin, txpin);

//----------------DEFINIZIONE MESSAGGIO TX--------------------
const byte Message_lenght = 36;
byte message[Message_lenght];
word Somma = 0;
word Checksum = 0;
boolean Message_OK = false ; 
const byte FINE_MSG_X = 15;
const byte FINE_MSG_Y = 240 ;

//------------------------DEFINIZIONE TIMER DEI RELE---------------------------------------
long T_ON_RELE_1A = -1;
long T_ON_RELE_2A = -1;
long T_ON_RELE_3B = -1;
long T_ON_RELE_4B = -1;
long T_ON_RELE_5C = -1;
long T_ON_RELE_6C = -1;
long T_ON_RELE_7D = -1;
long T_ON_RELE_8D = -1;
long nowTime;

unsigned int T_ON_RELE_1A_NEW;
unsigned int T_ON_RELE_2A_NEW;
unsigned int T_ON_RELE_3B_NEW;
unsigned int T_ON_RELE_4B_NEW;
unsigned int T_ON_RELE_5C_NEW;
unsigned int T_ON_RELE_6C_NEW;
unsigned int T_ON_RELE_7D_NEW;
unsigned int T_ON_RELE_8D_NEW;
//--------------------TIMER AGGIRNAMENTO STATO------------------------------------
const int SEND_Time = 64;
boolean UPDATE_OK = false ;

//-------------------WATCHDOG-----------------------------------------------------
#include <avr/wdt.h>  // inclusione libreria watchdog 

//----------------ALTRE VARIABILI-------------------------------------
static unsigned int  Cyclecounter = 0;
int i;                          // variabile indice per conteggio

//-----------------------------SETUP-----------------------------------------------

void setup () {

  Serial.begin(Seriale_Radio);
  Serial.print("OSIRELE_10GEN2023_v2");
  Serial.print("   ID: ");

  Serial.print(ID_NODE_1);
  Serial.print(ID_NODE_2);
  Serial.print(ID_NODE_3);
  Serial.print(ID_NODE_4);
  Serial.print(ID_NODE_5);
  Serial.println(ID_NODE_6);

  randomSeed(analogRead(0)); 
 
  pinMode(CMD_RELE_1A, OUTPUT); // pin definition
  pinMode(CMD_RELE_2A, OUTPUT); // pin definition
  pinMode(CMD_RELE_3B, OUTPUT); // pin definition
  pinMode(CMD_RELE_4B, OUTPUT); // pin definition
  pinMode(CMD_RELE_5C, OUTPUT); // pin definition
  pinMode(CMD_RELE_6C, OUTPUT); // pin definition
  pinMode(CMD_RELE_7D, OUTPUT); // pin definition
  pinMode(CMD_RELE_8D, OUTPUT); // pin definition
 
  digitalWrite( CMD_RELE_1A, LOW ); 
  digitalWrite( CMD_RELE_2A, LOW ); 
  digitalWrite( CMD_RELE_3B, LOW ); 
  digitalWrite( CMD_RELE_4B, LOW ); 
  digitalWrite( CMD_RELE_5C, LOW ); 
  digitalWrite( CMD_RELE_6C, LOW ); 
  digitalWrite( CMD_RELE_7D, LOW ); 
  digitalWrite( CMD_RELE_8D, LOW );
}

//-----------------------------LOOP------------------------------------------------
//-----------------------------LOOP------------------------------------------------
//-----------------------------LOOP------------------------------------------------

void loop () {
  
  SoftwareSerial BEE_Serial(rxpin, txpin);
  BEE_Serial.begin(Seriale_Radio);  //radio baud rate
  Serial.begin(Seriale_Radio);
  wdt_reset();  // resetta il timer del watchdog
  Serial.flush();
  //pinMode(POWER_SENS_D2,OUTPUT);
  pinMode(POWER_BEE, OUTPUT); // setto il pin 5 POWER_BEE come output
  //pinMode(POWER_BEE,INPUT);
  //digitalWrite(SET_RADIO, LOW);
  digitalWrite(POWER_BEE, HIGH);   // sets the POWER_BEE on
  //delay(DELAY_BEE_ON);                  // ritardo per stabilizzare  
  //----------FORZA COMANDI-------------------------------
  /*
  digitalWrite( CMD_RELE_1A, LOW ); 
  digitalWrite( CMD_RELE_2A, LOW ); 
  digitalWrite( CMD_RELE_3B, LOW ); 
  digitalWrite( CMD_RELE_4B, LOW ); 
  digitalWrite( CMD_RELE_5C, LOW ); 
  digitalWrite( CMD_RELE_6C, LOW ); 
  digitalWrite( CMD_RELE_7D, LOW ); 
  digitalWrite( CMD_RELE_8D, LOW );
  */
 
  // ---------------------------------------

  delay (3000);

  Cyclecounter ++; 

  //Serial.print("Cyclecounter=");
  //Serial.println(Cyclecounter, DEC);   
  if(Cyclecounter >= 201){Cyclecounter = 0; }  
  wdt_reset();  // resetta il timer del watchdog
  i=0;

  if (BEE_Serial.available() > 0) {
    Serial.print(" Bytes ricevuti= ");
    Serial.println(BEE_Serial.available(), DEC); 
  }

  //1-------------RICEZIONE E CONTROLLO CORRETTEZZA MESSAGGIO RADIO-----------------------------------------------

  while (BEE_Serial.available() > 0){   
    message[i]=BEE_Serial.read ();  // se ci sono caratteri da leggere sulla seriale leggili tutti e mettili nell'array
    // Serial.print(i, DEC);
    // Serial.print("=");
    // Serial.println(message[i], HEX); 

    // Serial.print(message[i]);
    // Serial.print(" ");

    i=i+1;
    
    if (i>=Message_lenght) {     
      i=0;
      break;
    } 
  
  } // end while

  BEE_Serial.flush();

  // Serial.println(message[58]);
  // Serial.println(message[59]);

  // controllo caratteri di fine frame
  if (message[Message_lenght-2] == 0x0F && message[Message_lenght-1] == 0xF0) {  
    // Serial.println("Ricezione messaggio da OsiGATE = "); // DA COMMENTARE DOPO TEST
    Somma=0;
    for (i=0; i < Message_lenght-4 ; i = i + 1) { Somma=Somma + message[i]; }
    // Serial.print("Somma = "); Serial.println(Somma, DEC);
    Checksum = word(message[32],message[33]);
    // Serial.print("Checksum = "); Serial.println(Checksum, DEC);
    if ( Checksum == Somma && ID_NODE_1==char(message[0]) && ID_NODE_2==char(message[1]) && ID_NODE_3==char(message[2]) && ID_NODE_4==char(message[3])&& ID_NODE_5==char(message[4]) && ID_NODE_6==char(message[5])) // controllo corretteza del messaggio con checksum 
    {
      // Serial.println("Messaggio corretto da OsiGATE = ");  // DA COMMENTARE DOPO TEST
      Message_OK = true;
    }
  } 

  //1---------------------------------------END RICEZIONE E CONTROLLO CORRETTEZZA MESSAGGIO RADIO------------------------------

  //2---------------------------------------AGGIORNAMENTO STATO DEI RELE------------------------------
  
  if (Message_OK) {  
    if (message[8]  == 0xFF){ digitalWrite( CMD_RELE_1A, HIGH );   }  else { digitalWrite( CMD_RELE_1A, LOW );     }
    if (message[11] == 0xFF){ digitalWrite( CMD_RELE_2A, HIGH );   }  else { digitalWrite( CMD_RELE_2A, LOW );     } 
    if (message[14] == 0xFF){ digitalWrite( CMD_RELE_3B, HIGH );   }  else { digitalWrite( CMD_RELE_3B, LOW );     }
    if (message[17] == 0xFF){ digitalWrite( CMD_RELE_4B, HIGH );   }  else { digitalWrite( CMD_RELE_4B, LOW );     }
    if (message[20] == 0xFF){ digitalWrite( CMD_RELE_5C, HIGH );   }  else { digitalWrite( CMD_RELE_5C, LOW );     }
    if (message[23] == 0xFF){ digitalWrite( CMD_RELE_6C, HIGH );   }  else { digitalWrite( CMD_RELE_6C, LOW );     }
    if (message[26] == 0xFF){ digitalWrite( CMD_RELE_7D, HIGH );   }  else { digitalWrite( CMD_RELE_7D, LOW );     }
    if (message[29] == 0xFF){ digitalWrite( CMD_RELE_8D, HIGH );   }  else { digitalWrite( CMD_RELE_8D, LOW );     }
  }
    
  //2---------------------------------------END AGGIORNAMENTO STATO DEI RELE------------------------------

  //3----------LEGGI E STAMPA STATO RELE-------------------------------

  if (Message_OK || MostraStatus) {
    if (!digitalRead(CMD_RELE_1A)) { Serial.println("RELE_1A=OFF ");  } else { Serial.println("RELE_1A=ON ");   }
    if (!digitalRead(CMD_RELE_2A)) { Serial.println("RELE_2A=OFF ");  } else { Serial.println("RELE_2A=ON ");   }
    if (!digitalRead(CMD_RELE_3B)) { Serial.println("RELE_3B=OFF ");  } else { Serial.println("RELE_3B=ON ");   }
    if (!digitalRead(CMD_RELE_4B)) { Serial.println("RELE_4B=OFF ");  } else { Serial.println("RELE_4B=ON ");  }
    if (!digitalRead(CMD_RELE_5C)) { Serial.println("RELE_5C=OFF ");  } else { Serial.println("RELE_5C=ON ");   }
    if (!digitalRead(CMD_RELE_6C)) { Serial.println("RELE_6C=OFF ");  } else { Serial.println("RELE_6C=ON ");   }
    if (!digitalRead(CMD_RELE_7D)) { Serial.println("RELE_7D=OFF ");  } else { Serial.println("RELE_7D=ON ");   }
    if (!digitalRead(CMD_RELE_8D)) { Serial.println("RELE_8D=OFF ");  } else { Serial.println("RELE_8D=ON ");  }
  }

  // ----------END LEGGI E STAMPA STATO RELE----------------------------- */
  
  //3---------------------------------------AGGIORNAMENTO TIMER DEI RELE------------------------------

  if (Message_OK) { 
    T_ON_RELE_1A_NEW = word (message[9] , message[10]);
    if (T_ON_RELE_1A_NEW != 65535) { 
      T_ON_RELE_1A = T_ON_RELE_1A_NEW*1000*60;
      T_ON_RELE_1A = T_ON_RELE_1A+millis();
    }
    
    T_ON_RELE_2A_NEW =  word (message[12], message[13]);
    if (T_ON_RELE_2A_NEW != 65535) { 
      T_ON_RELE_2A = T_ON_RELE_2A_NEW*1000*60;
      T_ON_RELE_2A = T_ON_RELE_2A+millis();
    }
    
    T_ON_RELE_3B_NEW = word (message[15], message[16]);
    if (T_ON_RELE_3B_NEW != 65535) { 
      T_ON_RELE_3B = T_ON_RELE_3B_NEW*1000*60;
      T_ON_RELE_3B = T_ON_RELE_3B+millis();
    }
    
    T_ON_RELE_4B_NEW = word (message[18], message[19]);
    if (T_ON_RELE_4B_NEW != 65535) { 
      T_ON_RELE_4B = T_ON_RELE_4B_NEW*1000*60;
      T_ON_RELE_4B = T_ON_RELE_4B+millis();
    }
    
    T_ON_RELE_5C_NEW = word (message[21], message[22]);
    if (T_ON_RELE_5C_NEW != 65535) { 
      T_ON_RELE_5C = T_ON_RELE_5C_NEW*1000*60;
      T_ON_RELE_5C = T_ON_RELE_5C+millis();
    }
    
    T_ON_RELE_6C_NEW = word (message[24], message[25]);
    if (T_ON_RELE_6C_NEW != 65535) { 
      T_ON_RELE_6C = T_ON_RELE_6C_NEW*1000*60;
      T_ON_RELE_6C = T_ON_RELE_6C+millis();
    }
    
    T_ON_RELE_7D_NEW = word (message[27], message[28]);
    if (T_ON_RELE_7D_NEW != 65535) { 
      T_ON_RELE_7D = T_ON_RELE_7D_NEW*1000*60;
      T_ON_RELE_7D = T_ON_RELE_7D+millis();
    }
    
    T_ON_RELE_8D_NEW = word (message[30], message[31]);
    if (T_ON_RELE_8D_NEW != 65535) { 
      T_ON_RELE_8D = T_ON_RELE_8D_NEW*1000*60;
      T_ON_RELE_8D = T_ON_RELE_8D+millis();
    }

    // Serial.println(message[9], HEX); Serial.println(message[10], HEX); Serial.println(word (message[9], message[10])); Serial.println(word (message[9], message[10]) * 1000 * 60);
    // Serial.println(T_ON_RELE_1A); Serial.println(T_ON_RELE_2A); Serial.println(T_ON_RELE_3B); Serial.println(T_ON_RELE_4B); Serial.println(T_ON_RELE_5C); Serial.println(T_ON_RELE_6C); Serial.println(T_ON_RELE_7D); Serial.println(T_ON_RELE_8D);
  
  }

  //3---------------------------------------END AGGIORNAMENTO TIMER DEI RELE------------------------------
  
  //Serial.print("millis= ");Serial.println(millis(), DEC);
  //Serial.print("T_ON_RELE_1A= ");Serial.println(T_ON_RELE_1A, DEC);
  wdt_reset();  // resetta il timer del watchdog
  //delay(5000);
  
  //4---------------------------------------MESSAGGIO RADIO DI ACK ------------------------------
  
  if (Message_OK) { 
      
    // message[0] = ID_NODE_1; STESSO DEL MSG RICEVUTO
    // message[1] = ID_NODE_2; STESSO DEL MSG RICEVUTO
    // message[2] = ID_NODE_3; STESSO DEL MSG RICEVUTO
    // message[3] = ID_NODE_4; STESSO DEL MSG RICEVUTO
    // message[4] = ID_NODE_5; STESSO DEL MSG RICEVUTO
    // message[5] = ID_NODE_6; STESSO DEL MSG RICEVUTO
    // message[6] STESSO RANDOM CODE DEL MSG RICEVUTO
    // message[7] STESSO RANDOM CODE DEL MSG RICEVUTO
    // Serial.print("message[6]= ");Serial.println(message[6], HEX);
    // Serial.print("message[7]= ");Serial.println(message[7], HEX);
    if (digitalRead(CMD_RELE_1A)) { message[8]=255;   }  else { message[8]=0;   }
    if (digitalRead(CMD_RELE_2A)) { message[11]=255;   } else { message[11]=0;   }
    if (digitalRead(CMD_RELE_3B)) { message[14]=255;   } else { message[14]=0;   }
    if (digitalRead(CMD_RELE_4B)) { message[17]=255;   } else { message[17]=0;   }
    if (digitalRead(CMD_RELE_5C)) { message[20]=255;   } else { message[20]=0;   }
    if (digitalRead(CMD_RELE_6C)) { message[23]=255;   } else { message[23]=0;   }
    if (digitalRead(CMD_RELE_7D)) { message[26]=255;   } else { message[26]=0;   }
    if (digitalRead(CMD_RELE_8D)) { message[29]=255;   } else { message[29]=0;   }

    Somma=0;
    for (i=0; i < Message_lenght-4 ; i = i + 1) { Somma=Somma + message[i]; }
    message[32] = highByte(Somma); 
    message[33] = lowByte(Somma); 
    message[34] = 240;
    message[35] = 15;
    for (i = 0; i < Message_lenght ; i = i + 1) {BEE_Serial.write(message[i]);}  //  trasmissione messaggio ACK_1
    //Serial.println("MESSAGGIO RADIO DI ACK - SPEDITO ");
    delay (1000);
    for (i = 0; i < Message_lenght ; i = i + 1) {BEE_Serial.write(message[i]);}  //  trasmissione messaggio ACK_2
    
    Message_OK = false;  // compiute tutte le azioni in seguito a messaggio ricevuto OK, si resetta il flag
      
  }
    
  //4---------------------------------------END MESSAGGIO RADIO DI AGGIORNAMENTO STATO------------------------------
  
  //5---------------------------------------CHECK TIMER DEI RELE------------------------------
  
  if (!Message_OK) { 
    nowTime = millis();
    if (T_ON_RELE_1A >= 0 and nowTime > T_ON_RELE_1A) { T_ON_RELE_1A = -1; if (digitalRead(CMD_RELE_1A)) { digitalWrite( CMD_RELE_1A, LOW );  Serial.println("RELE_1A=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_2A >= 0 and nowTime > T_ON_RELE_2A) { T_ON_RELE_2A = -1; if (digitalRead(CMD_RELE_2A)) { digitalWrite( CMD_RELE_2A, LOW );  Serial.println("RELE_2A=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_3B >= 0 and nowTime > T_ON_RELE_3B) { T_ON_RELE_3B = -1; if (digitalRead(CMD_RELE_3B)) { digitalWrite( CMD_RELE_3B, LOW );  Serial.println("RELE_3B=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_4B >= 0 and nowTime > T_ON_RELE_4B) { T_ON_RELE_4B = -1; if (digitalRead(CMD_RELE_4B)) { digitalWrite( CMD_RELE_4B, LOW );  Serial.println("RELE_4B=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_5C >= 0 and nowTime > T_ON_RELE_5C) { T_ON_RELE_5C = -1; if (digitalRead(CMD_RELE_5C)) { digitalWrite( CMD_RELE_5C, LOW );  Serial.println("RELE_5C=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_6C >= 0 and nowTime > T_ON_RELE_6C) { T_ON_RELE_6C = -1; if (digitalRead(CMD_RELE_6C)) { digitalWrite( CMD_RELE_6C, LOW );  Serial.println("RELE_6C=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_7D >= 0 and nowTime > T_ON_RELE_7D) { T_ON_RELE_7D = -1; if (digitalRead(CMD_RELE_7D)) { digitalWrite( CMD_RELE_7D, LOW );  Serial.println("RELE_7D=OFF "); } } // Se scaduto il timer spegni il relè
    if (T_ON_RELE_8D >= 0 and nowTime > T_ON_RELE_8D) { T_ON_RELE_8D = -1; if (digitalRead(CMD_RELE_8D)) { digitalWrite( CMD_RELE_8D, LOW );  Serial.println("RELE_8D=OFF "); } } // Se scaduto il timer spegni il relè     
  }
  
  //5---------------------------------------END CHECK TIMER DEI RELE------------------------------
  wdt_reset();  // resetta il timer del watchdog

  //6---------------------------------------MESSAGGIO RADIO DI STATO------------------------------
  // Serial.println(Cyclecounter);
  if (!Message_OK  && Cyclecounter % SEND_Time == 0) { 
    message[0] = ID_NODE_1;
    message[1] = ID_NODE_2; 
    message[2] = ID_NODE_3;
    message[3] = ID_NODE_4;
    message[4] = ID_NODE_5;
    message[5] = ID_NODE_6;
    message[6] = 0;
    message[7] = 0;
  
    if (digitalRead( CMD_RELE_1A))  {message[8] =  255 ;}  else {message[8] = 0 ;} 
    if (digitalRead( CMD_RELE_2A))  {message[11] = 255 ;} else {message[11] = 0 ;} 
    if (digitalRead( CMD_RELE_3B))  {message[14] = 255 ;} else {message[14] = 0 ;} 
    if (digitalRead( CMD_RELE_4B))  {message[17] = 255 ;} else {message[17] = 0 ;} 
    if (digitalRead( CMD_RELE_5C))  {message[20] = 255 ;} else {message[20] = 0 ;} 
    if (digitalRead( CMD_RELE_6C))  {message[23] = 255 ;} else {message[23] = 0 ;} 
    if (digitalRead( CMD_RELE_7D))  {message[26] = 255 ;} else {message[26] = 0 ;} 
    if (digitalRead( CMD_RELE_8D))  {message[29] = 255 ;} else {message[29] = 0 ;} 
    
    Somma=0;
    for (i=0; i < Message_lenght-4 ; i = i + 1) { Somma=Somma + message[i]; }
    message[32] = highByte(Somma); 
    message[33] = lowByte(Somma); 
    message[34] = 240;
    message[35] = 0xF;

    for (i = 0; i < Message_lenght ; i = i + 1) {BEE_Serial.write(message[i]);}
  
  
    //delay(1000);
    //Serial.println("MESSAGGIO RADIO DI STATO - SPEDITO ");
    //for (i = 0; i < Message_lenght ; i = i + 1) { Serial.print(i, DEC); Serial.print("="); Serial.println(message[i], HEX); } 
  }

  //6---------------------------------------END MESSAGGIO RADIO INFORMAZIONE STATO RELE------------------------------

  Message_OK =false ;
  
  wdt_reset();  // resetta il timer del watchdog
  delay(250);

  //--------------------------------------------

  //wdt_reset();  // resetta il timer del watchdog

  //delay (DELAY_BEE_OFF);
  //digitalWrite(POWER_BEE, LOW);   // sets the POWER_BEE on

  //wdt_reset();  // resetta il timer del watchdog

} //---------------------------END LOOP------------------------------------------------
