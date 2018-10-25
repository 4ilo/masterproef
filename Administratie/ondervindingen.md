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