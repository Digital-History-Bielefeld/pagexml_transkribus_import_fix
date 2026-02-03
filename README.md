# pagexml_transkribus_import_fix
This tool allows you to convert PAGE xml 2019 files to 2013 aka it allows you to convert PAGE XML from eScriptorium to fit the Transkribus guidelines.
This is done by:
1.  changing the namespace and reference of the xml format.
2.  updating the reading order if it is not set
3.  setting region and line types if they are empty
This should create a file you can upload as PAGE xml with your images.

# Rundown of how to use
1.  Export your image and xml from eScriptorium.
2.  Set the location of the donwloaded files in the script such that the folder is selected with the images inside and a imaginary folder inside it named page (to mimick Transkribus file structure, otherwise you can't import xml...).
3.  Run the script.
4.  Import the files in Transkribus the way you would upload any images. It should be significantly slower and should automatically link your xmls.

# Potential Issues
The format you want could be something else than this converter allows, because it changed etc.
