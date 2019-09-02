This python (V3.7.3) script is a simple crawler/parser specifically for the German news website www.spiegel.de.
It extracts all links from the homepage HTML, throws out everything that is not a "real" article (i.e.
advertisements, sports livetickers, forum discussions and Bento, the kids version of Spiegel) and downloads
the HTML for the articles and saves them as .txt files. It then extracts some info about the articles
(author, resort, time and date, ...) and saves it in a .csv file.
As of now it is hardcoded to work specifically with spiegel.de, but if you take a look at the HTML source
of other news webistes, you can change the "filters" for the article links as well as the search terms for
finding the article metadata. I wrote this program after I saw the 33c3 talk "SpiegelMining"
(https://www.youtube.com/watch?v=-YpwsdRKt8Q) and wanted to try some of the things myself, so I made this tool
to make my own dataset.

To run this script you just need to put it in some folder (you can even run it from your desktop, if you want to)
and run it from the command line. If you're feeling fancy, run it through Sublime Text or something. The script
will run until there's a keyboard interrupt.
