import os
import xml.etree.ElementTree as ET

# --- CONFIGURATION ---
input_folder = r'C:\Users\Nisam\Desktop\Import' 
output_folder = r'C:\Users\Nisam\Downloads\export\page'
image_extension = ".jpg"  # Ensure this matches your image files exactly

# Namespaces
NS_2013 = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
NS_2019 = "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
ET.register_namespace('', NS_2013)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.xml') and filename.upper() != 'METS.XML':
        file_path = os.path.join(input_folder, filename)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            if 'PcGts' not in root.tag: continue

            print(f"Processing: {filename}")

            # 1. Fix Namespaces
            for el in root.iter():
                if el.tag.startswith("{" + NS_2019 + "}"):
                    el.tag = el.tag.replace(NS_2019, NS_2013)

            # 2. Fix Schema Location
            root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", 
                     f"{NS_2013} {NS_2013}/pagecontent.xsd")

            # 3. Fix Image Filename Reference
            page_el = root.find(f".//{{{NS_2013}}}Page")
            if page_el is not None:
                # Force imageFilename to match the expected jpg name
                real_img_name = filename.replace(".xml", image_extension)
                page_el.set("imageFilename", real_img_name)

            # 4. Fix TextRegions and Baselines
            regions = root.findall(f".//{{{NS_2013}}}TextRegion")
            for reg in regions:
                reg.set('type', 'paragraph') # Ensure type exists
                
                # Check all Baselines for single-point errors
                lines = reg.findall(f".//{{{NS_2013}}}TextLine")
                for line in lines:
                    baseline = line.find(f"{{{NS_2013}}}Baseline")
                    if baseline is not None:
                        points = baseline.get("points", "").split(" ")
                        if len(points) < 2:
                            # Transkribus crashes on 1-point lines. 
                            # We duplicate the point to make it a tiny line.
                            baseline.set("points", f"{points[0]} {points[0]}")

            # 5. Fix ReadingOrder
            ro = root.find(f".//{{{NS_2013}}}ReadingOrder")
            if ro is None and page_el is not None:
                ro = ET.Element(f"{{{NS_2013}}}ReadingOrder")
                og = ET.SubElement(ro, f"{{{NS_2013}}}OrderedGroup", id="ro_1", caption="Reading order")
                for i, reg in enumerate(regions):
                    ET.SubElement(og, f"{{{NS_2013}}}RegionRefIndexed", index=str(i), regionRef=reg.get('id'))
                page_el.insert(0, ro)

            # 6. Save with the MANDATORY double extension
            new_filename = filename
            tree.write(os.path.join(output_folder, new_filename), encoding="UTF-8", xml_declaration=True)
            
        except Exception as e:
            print(f"Error on {filename}: {e}")

print("\nDone! Please use the files in the 'transkribus_ready' folder.")