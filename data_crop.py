import os
import cv2
import xml.etree.ElementTree as ET

# Setze die Pfade entsprechend deines Projekts
xml_file_path = 'annotations.xml'
base_directory = 'images_final'  # Zielverzeichnis für die geschnittenen Bilder
raw_images_directory_april = 'images\\2023Apfel\\April&Mai-Bilder-CVAT\\\April Tag\\Tag'  # Ursprüngliches Bilderverzeichnis April
raw_images_directory_mai = 'images\\2023Apfel\\April&Mai-Bilder-CVAT\\Mai Tag\\Tag'  # Ursprüngliches Bilderverzeichnis Mai



# XML-Datei parsen
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Gehe jede Bildannotation durch
for image in root.findall('image'): #Sucht im XML-Root nach allen Elementen, die das Tag <image>
    image_name = image.get('name') #Hier wird der name-Attribut des aktuellen <image>-Tags ausgelesen
    image_name = image_name.split("/")[-1]


    image_path = os.path.join(raw_images_directory_april, image_name) #Mit os.path.join() wird der vollständige Pfad zur Bilddatei zusammengesetzt.
    img = cv2.imread(image_path) #Lädt das Bild von der Festplatte in den Speicher
    
    if img is None:
        print(f"Das Bild {image_name} konnte nicht geladen werden. Path: {image_path}")
        continue

    # Verarbeite jedes Polygon (Label)
    for index,polygon in enumerate(image.findall('polygon')):#Schleife, um jedes <polygon>-Element im aktuellen <image>-Element zu durchlaufen
        bbch = polygon.find('attribute').text #Code liest den Text des Attributes aus
        points = polygon.get('points').split(';') # Koordinatenpunkte des Polygons, die als Zeichenkette gespeichert sind, ausgelesen und bei jedem Semikolon (;) geteilt
        points = [list(map(lambda x: int(float(x)), point.split(','))) for point in points] #Jeder Punkt wird bei jedem Komma gespalten, um die x- und y-Koordinaten zu trennen.
                                                                        #Die map(int, point.split(',')) Funktion wandelt die gesplitteten String-Koordinaten in Integer um,
                                                                        # und list(...) wandelt das Ergebnis in eine Liste von Koordinaten um. Dies wiederholt sich für jeden Punkt,
                                                                        #sodass points eine Liste von Listen wird, wobei jede innere Liste ein Paar von x- und y-Koordinaten enthält
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points] #Extrahieren der x- und y-Koordinaten in separate Listen, indem sie die ersten (Index 0) bzw. zweiten (Index 1) Elemente
                                          # aus jeder Koordinatenliste in points holen
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords) #Bounding Box Koords

        # Bilde die Bounding Box aus dem Polygon und schneide das Bild zu
        cropped_img = img[y_min:y_max, x_min:x_max]

        # Zielordner erstellen, falls nicht vorhanden
        folder_path = os.path.join(base_directory, f"BBCH {bbch}")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        
        # Zielbildpfad
        cropped_image_path = f'{folder_path}/{image_name.split(".")[0]}_{str(index)}.jpg'


        # Bild speichern
        cv2.imwrite(cropped_image_path, cropped_img)
        print(f'Bild {cropped_image_path} gespeichert')

print('Verarbeitung abgeschlossen.')
