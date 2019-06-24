## 5.1 

a)
Software switch
- Openflow features erst nachträglich hinzugefügt
- Meisten Operationen nur über Software

Hardware switch
- Meisten Operationen in hardware umgesetzt
- schneller und energiesparender
- Optimiert auf Openflow tabellen

Device: mix

b)
Vacancy events: 

- TCAM Speicher, endlich, gefüllt mit flow entries
- vacancy threshold: Übergangsgrenze
    - Switch sagt controller bescheid, dass bald voll ist
    - Mit Umgebung darum, damit das event nicht ständig getriggered wird

- Ohne die Events merkt man das erst zu spät

c)
- TCAM Speicher: Kann für bit strings direkt entscheiden ob drin oder nicht
- Vergleichswerte aus flow tabelle darin abspeichern, dann pointer zu den aktionen die durchgeführt werden
- Zugriff bleibt O(1)
- Andere Aufgaben da auch mit rein
- Dont care bits (mit x)
- Binary CAM: nur 0 oder 1, Tenary CAM (TCAM) kann auch dont care bits
- TCAM teurer

## 5.2) NOS AND SDN Languages

a) 
- Distributed State: Verteilung des states geschieht automatisch, kann an einer stelle geändert werden und wird auf die switchtes verteilt
- Specification? Einfachere Programmierbarkeit
    - z.B: Pyretic language

b)
Nutzen von Abstraktionen

d)
- SDM wird hier gemacht, eine Art overlay multicast der software defined ist
    - Hier fehlen noch bestimmte Gruppen für SDM 
- Möglich evtl streaming oder sowas
