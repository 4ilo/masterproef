# Ondervindigen en resultaten

### 22/10 Experiment met gPb algoritme:
- Uit paper Contour detection & Hierarchical image segmentation - Pablo Arbeláez
- Mooi segmentatie resultaat
- Heeeeel traag (meerdere minuten per beeld)

### 22/10 Experiment met k-means segmentation
- Gangen zijn in eerste instantie moeilijk met k-means te detecteren door de vele schaduwen/overbelichting

### 25/10 Experiment met sign-detection
- Tresholding tussen 2 hue waardes in combinatie met erosie+dilatie en contour detectie geeft een goed resultaat voor detectie van een bordje
- Het belichtingsverschil tussen de verschillende gangen is behoorlijk groot waardoor de treshold ruimer genomen moet worden
- Na het tekenen van de bounding boxes, zijn de gedetecteerde bordjes van te lage kwaliteit om sift features op te vinden

Bij het experimenteren met sign detectie heb ik geprobeerd om de hoogspanningsbordjes te detecteren. De eerste bemerking bij het omzetten van een beeld naar hsv is dat de beelden er redelijk vervuild uitzien. Op een image met enkel de hue uitgeplot is de locatie van de bordjes zeker te herkennen, maar er zijn ook andere vlekken die schijnbaar dezelfde kleur hebben.

Met een treshold range op de hue (waardes in de buurt van 20-30) is het alzeker mogelijk om de bordjes hun kleur te selecteren.
Na het toepassen van eem paar morphologische operaties(erosie+dilatie) en een contour detectie kon ik redelijk goede bounding boxes tekenen rondom de bordjes. Deze treshold range werkt ook op andere beelden uit dezelfde gang(verder af + dichter bij hetzelfde object). Hetzelfde pictogram hangt ook in de volgende gang, maar de belichting is daar volledig anders waardoor de kleur afwijkt. Om beide situaties te kunnen detecteren heb ik de range vergroot, maar dan komen er ook meer andere detecties in het beeld op plaatsen waar de hue vervuild is.

Als 2de stap heb ik reeds geprobeerd om in de gedetecteerde area SIFT features te detecteren. Dit is momenteel echter niet een groot success omdat er weinig features gedetecteerd worden. Ik veronderstel dat dit is omdat de resolutie van de afbeeldingen niet zo goed zijn. Dit moet nog verder bekeken worden.


# 8/11 Experimenten met segmentatie
- Segnet zeer moeilijk werkend te krijgen
- Een andere indoor-segmentatie [framework](https://github.com/hellochick/Indoor-segmentation) gebaseerd op tensorflow is een oplossing, en geeft een goed resultaat voor muren en vloeren
