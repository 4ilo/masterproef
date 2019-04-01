# Masterproef "Visie voor semantische robotnavigatie in ziekenhuisgangen"

## Logboek

| Datum | Activiteit |
| ----- | ---------- |
| 1/10/18 | Opzoekwerk literatuur voor masterproef |
| 4/10/18 | Opzoekwerk literatuur voor masterproef |
| 8/10/18 | Opzoekwerk literatuur voor masterproef |
| 9/10/18 | Vergadering over masterproef met Toon Goedemé & Filip Reniers|
| 9/10/18 | Maken inloopverslag |
| 11/10/18 | Opzoekwerk literatuur voor masterproef |
| 15/10/18 | Opzoekwerk literatuur voor masterproef |
| 18/10/18 | Opzoekwerk literatuur voor masterproef |
| 18/10/18 | Eenvoudige experimenten met SIFT & yolo |
| 18/10/18 | Skypemeeting met Filip Reniers |
| 21/10/18 | Opzoekwerk literatuur over sign detection & SIFT object tracking |
| 22/10/18 | Experimenten met gPb algoritme & k-means segmentatie|
| 22/10/18 | Skypemeeting met Filip Reniers |
| 25/10/18 | Experiment met sign-detection |
| 27/10/18 | Experimenten met sign-detection |
| 28/10/18 | Onderzoek naar segemetatietechnieken voor indoor |
| 29/10/18 | Experimenten voor segmentatie |
| 30/10/18 | Vergadering Toon Goedemé |
| 30/10/18 | Start anotatie beelden |
| 31/10/18 | Anotaie beelden + hertrainen yolo |
| 6/11/18 | Skype meeting met Filip Reniers |
| 8/11/18 | Experimenten met indoor segmentatie|
| 12/11/18 | Opstellen activiteitenrapport 1 |
| 12/11/18 | Verder onderzoek image segmentatie |
| 14/11/18 | Skype meeting met Filip Reniers |
| 19/11/18 | Begin schrijven literatuurstudie |
| 22/11/18 | Verder onderzoek literatuurstudie |
| 26/11/18 | Verder schrijven literatuurstudie |
| 3/12/18 | Verder schrijven literatuurstudie |
| 6/12/18 | Verder schrijven literatuurstudie |
| 9/12/18 | Literatuurstudie |
| 10/12/18 | Literatuurstudie |
| 13/12/18 | Hoofdstuk reeds gerealiseerd |
| 17/12/18 | Afwerken tussentijds verslag |
| 1/02/19 | Tussentijdse presentatie |
| 14/02/19 - 28/02/19 | Annoteren beeldmateriaal |
| 20/02/19 | Bespreken tussentijdse resultaten met Toon Goedemé |
| 1/03/19 - 14/03/19 | Hertrainen object detector |
| 13/03/19 | Bespreken activiteitenrapport2 met Toon Goedemé |
| 14/03/19 | Beginnen perspectiefpunt detectie |
| 15/03/19 | Perspectiefdetectie + Skype meeting Filip |
| 22/03/19 | Perspectiefdetectie |
| 23/03/19 | Visualisatie jsom formaat |
| 24/03/19 | Experimenten met yolo training |
| 28/03/19 | Uitdenken + experimenteren wiskunde voor afstanden naar hoeken |
| 29/03/19 | Implementatie berekening hoeken |
| 30/03/19 | Maken tekening hoeken berekening |

## Originele omschrijving
Het doel van deze thesis is om een set van feature detectors te selecteren en configureren om de samenstellende componenten/onderdelen van objecten te herkennen. 
Meerbepaald de objecten die terug te vinden zijn in de gangen van de logistieke vloer van een ziekenhuis.

De context van de thesis:
Bestaande ziekenhuizen hebben een grote nood aan automatisatie van hun textiellogistiek en goederenstromen, zodat het zorgpersoneel meer tijd aan zorg kan spenderen. Deze automatisatie staat nog niet ver omdat het niet mogelijk is om de volledige infrastructuur aan te passen zoals in de industrie (bv: transportbanden) en omdat er al een hoop logistiek materiaal voorhanden is. 
Een Autonoom Geleid Voertuig (AGV) kan gebruikt worden om bestaand logistiek materiaal (karren en bedden) autonoom te verplaatsen binnen de logistieke vloer van het ziekenhuis.

Dit voertuig moet kunnen navigeren in deze gangen en moet weten in wat voor situatie hij zich bevindt. 
Hij is daarom voorzien van camera’s om de omgeving te observeren en beschikt over een interne ‘semantische’ kaart  waarop aangeduid is waar hij welke zaken (muren,deuren, buizen, bordjes, verlichting, ...) kan verwachen in de ziekenhuisgang. 
Deze kaart bestaat uit tags die verwijzen naar objecten met een ruwe schatting van afmetingen, positie en oriëntatie. 
De AGV zou met behulp van deze kaart de objecten in de echte wereld herkennen. 
De kennis in deze kaart kan gebruikt worden om een zoekruimte in het beeldvlak af te bakenen. 
Dit is waar het werk van de thesis start.te bakenen. Dit is waar het werk van de thesis start.