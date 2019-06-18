from bs4 import BeautifulSoup
import os, glob

def file_replace_text(fname, toreplace, replacement):
    print("opening " + fname)
    with open(fname, 'r',  encoding='Windows-1252') as file:
        filedata = file.read()
    # Replace the text in file
    filedata = filedata.replace(toreplace, replacement)
    # Write the file out again
    with open(fname, 'w') as file:
        file.write(filedata)

def main():
    KBID = str(input("Enter KB number to beautify: "))
    dirname = os.path.dirname(__file__)
    # print(dirname)
    folderpath = os.path.join(dirname, KBID)
    # print(folderpath)

    # list all .html files in chosen directory (there should only be one)
    os.chdir(folderpath)
    for file in glob.glob('*.html'):
        filename = file

    filepath = os.path.join(folderpath, filename)

    print ("Cleaning " + filename)

    #removing smart quotes
    file_replace_text(filepath, '“', '"')
    file_replace_text(filepath, '”', '"')

    #start html cleaning with beautifulsoup
    with open(filepath, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, "html.parser")

    #saves title name for later
    title = soup.title.get_text()
    print(title)

    #remove style tag from header
    soup.find('style').extract()

    #remove unnecessary attributes
    for tag in soup():
        for attribute in ['class', 'id', 'name', 'style']:
            del tag[attribute]
    
    #changes image path for KB site
    for image in soup.findAll('img'):
        image['src'] = image['src'].replace(title, "/images/group87/"+KBID)

    #do string processing after here
    soup_string = str(soup)

    #removes all <p><br/></p> tags
    soup_string = soup_string.replace('<p><br/></p>', '<br/>')

    #encapsulates <p> tags in <body> with a <div>
    soup_string = soup_string.replace('<body>', '<body>\n<div>')
    soup_string = soup_string.replace('</body>', '</div>\n</body>')

    #exports file with .new at end
    with open(filepath+'.new', 'w') as file:
        file.write(str(soup_string))


if __name__ == "__main__":
    main()