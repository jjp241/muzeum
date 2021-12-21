# Muzeum
MIMUW BD (Databases) Project

#### Instalacja i uruchomienie testowe:
0. Musimy mieć zainstalowany `python` i `pip`
1. Instalacja pakietów: `pip install -r requirements.txt`
2. Uruchomienie aplikacji:
 ```
    export FLASK_APP=index.py 
    flask run
 ```
 I otwarcie odpowiedniego adresu w przeglądarce (w oknie terminala powinien być link)
3. Have fun :) Uwaga - na komputerze własnym może nie działać większość rzeczy jako że nie ma połączenia z bazą psql.

#### Uruchamiane na studentsie:
Lepiej uruchamiać na studentsie takimi samymi poleceniami (ale z poziomu studentsa) - wtedy powinno działać połączenie z bazą psql i w oknie terminala widzimy gdy coś nie działa.

#### Eksport do public_html:
Na studentsie repo sklonowane do jakiegoś podkatalogu `public_html` powinno działać out-of-the-box gdy wejdzie się tam adresem (bo jest skonfigurowany plik `index.cgi`
