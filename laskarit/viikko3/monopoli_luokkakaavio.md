```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Ruutu "*" -- "1" Toiminto
    Ruutu <|-- Aloitusruutu
    Ruutu <|-- Vankilaruutu
    Ruutu <|-- Sattumaruutu
    Ruutu <|-- Yhteismaaruutu
    Ruutu <|-- Asemaruutu
    Ruutu <|-- Laitosruutu
    Ruutu <|-- Normaalikaturuutu
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    class Monopolipeli{
        aloitusruudunSijainti
        vankilaruudunSijainti
    }
    class Normaalikaturuutu{
        kadunNimi
    }
```
