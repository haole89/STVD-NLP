# STVD-NLP
 This repo provided the codes to extract the information from XML metata of TV channels in France.
 
# Pre-processing with XML
The first step is the Pre-processing xml text to extract all of the TV programs during 06:00 AM to 02:00 AM of next day.
Input: the list of XML file with its names formatted yyyy-mm-dd_HHMMSS.xml
Ouput: The list of TV programs that provided for each day based on the name of the XML file.
For example: 
Input: The file 2022-01-01_100000.xml
Ouput: List of TV programs which its starts FROM at 06:00:00 01-01-2022 TO at 02:00:00 02-01-2022
Notes: Using SHA-1 hash function for robustness of TV titles.

# Trimming video based on the information that extracted.
Notes: Record video 20 hours per day (from 06:00 to 02:00 of next day)

