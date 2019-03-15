# Vergaderingen en Skype meetings

### Skype meeting Filip Reniers 18/10
- Verband tussen sift & localisatie verder onderzoeken
- Sift tracking (beperken zoekrange) verder onderzoeken
- Verder onderzoeken algoritmes(+zoeken nieuwere versies) bordjes/verkeersbord tracking
- Zoeken naar image segmentatie voor als er geen 'objecten' zijn


### Skype meeting Filip Reniers 22/10
- Bespreking bevindingen 21/10
- Deze week expirimenten uitvoeren met bordjes detector(Vrijdag 26/10 bevindingen)
- Afspraak maken met Toon Goedeme (bevindingen 26/10)
- Hsi/hsv is niet altijd optimale kleurbereik. Bij TL-licht is het moeilijk om nog juist te detecteren

- Over exposure bij lampen is ook een mogelijke feature
- Algemene doel: Toolbox van meerder detecors/trackers
- Detectors laten werken als versterking van elkaar:
    - X is gedetecteerd, nu weet ik dat ik op plaats y normaal z zou moeten kunnen zien, dus ik start detector voor z



### Vergadering Toon Goedemé
- Bespreking tot nu toe gericht onderzoek + bekomen resultaten
- De tot nu toe onderzochte technieken zullen waarschijnlijk niet tot een perfecte oplossing leiden.
- Er zal meer gekeken moeten worden naar CNN zoals YOLO voor detectie en naar Segnet voor segmentatie van deuren en vloeren.
- Het is misschien goed om een vergelijking te maken tussen CNN en traditionele technieken ter vergelijking.
- Yolo trainen voor het zoeken van: pictogrammen, bransblussers, hoeken, deurklinken
- Alle beelden moeten geannoteerd worden voor een hertraining van bijvoorbeeld YOLO. Tools hiervoor zijn:
    - openc: cvat/vatic
    - label-img
    - brambox


### Skype meeting Filip Reniers 6/11
- Bespreking bevindingen
- Opstellen van tutorial voor reproductie yolo resultaten
- Opzoeken over object tracking met yolo
- Verder bekijken hoe de actuele locatie gebruikt kan worden voor betere detectieresultaten
- Deze week kijken naar segnet voor segmentatie van muren, vloeren en deuren


### Skype meeting Filip Reniers 14/11
- Onderzoek naar Tracking
- Voorkennis (niet hele beeld scannen)


### Bespreking activiteitenrapport2 met Toon Goedemé 13/03
- Bespreking nieuwe planning
- Bespreking huidige resultaten (annotatie & training)
- Uitdenken strategie voor koppeling tussen object detector & objecten op kaart
- Methode besproken om pixel-afstanden van objecten tov het perspectiefpunt om te zetten naar hoeken
- Deze hoeken gebruiken om schatting van locatie te maken op basis van een semantische kaart
- Wetenschappelijke onderbouwing van paper verbeteren door deze methode te vergelijken met SLAM (ORB-SLAM, PTAM)

### Skype meeting Filip Reniers 15/03
- Bespreken resultaten tot nu toe
- Planning herwerken met nieuw besproken doelen
- Wiskunde neerschrijven
