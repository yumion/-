// 変数の定義
#define LED_PIN1 13
#define LED_PIN2 12
 
// 初期化
void setup(){
  pinMode(LED_PIN1, OUTPUT);
  pinMode(LED_PIN2, OUTPUT);
 
  // シリアルポートを9600 bps[ビット/秒]で初期化 
  Serial.begin(9600);
}
 
// 繰り返し処理
void loop(){
  int inputchar;
 
  // シリアルポートより1文字読み込む
  inputchar = Serial.read();
 
  if(inputchar != -1 ){
    // 読み込んだデータが -1 以外の場合　以下の処理を行う
 
    switch(inputchar){
      case '1':
        // 読み込みデータが　1 の場合
 
        Serial.print("LED RED ON\n");
        digitalWrite(LED_PIN1, HIGH);
        break;
        
      case '0':  
        // 読み込みデータが　0 の場合
 
        Serial.print("LED RED OFF\n");
        digitalWrite(LED_PIN1, LOW);
        break;

      case '3':
        // 読み込みデータが　3 の場合
 
        Serial.print("LED GREEN ON\n");
        digitalWrite(LED_PIN2, HIGH);
        break;
        
      case '2':  
        // 読み込みデータが　2 の場合
 
        Serial.print("LED GREEN OFF\n");
        digitalWrite(LED_PIN2, LOW);
        break;
    }
  } else {
    // 読み込むデータが無い場合は何もしない
  }
}
