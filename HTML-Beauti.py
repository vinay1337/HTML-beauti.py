from bs4 import BeautifulSoup
import os, glob, sys

def file_replace_text(fname, toreplace, replacement):
    #print("opening " + fname)
    with open(fname, 'r',  encoding='ANSI') as file:
        filedata = file.read()
    # Replace the text in file
    filedata = filedata.replace(toreplace, replacement)
    # Write the file out again
    with open(fname, 'w') as file:
        file.write(filedata)

def main():
    if len(sys.argv) <= 1:
        KBID = str(input("Enter KB number to beautify: "))
    else:
        print("ARG detected: "+sys.argv[1])
        KBID = sys.argv[1]
    
    dirname = os.path.dirname(__file__)
    # print(dirname)
    folderpath = os.path.join(dirname, KBID)
    # print(folderpath)

    # list all .html files in chosen directory (there should only be one)
    os.chdir(folderpath)
    for file in glob.glob('*.html'):
        filename = file
    os.chdir('..')

    filepath = os.path.join(folderpath, filename)

    print ("Cleaning " + filename)

    #removing smart quotes
    file_replace_text(filepath, '“', '"')
    file_replace_text(filepath, '”', '"')

    #start html cleaning with beautifulsoup
    with open(filepath, encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, "html.parser")

    #shameless self-promotion
    creditMe = soup.new_tag('meta', content='Converted to HTML by Vinay Janardhanam')
    soup.head.append(creditMe)

    #remove style tag from header
    for s in soup('style'):
        s.extract()

    #replace <h1> with <h3>
    for h1 in soup('h1'):
        h1.name = 'h3'

    #replace <h2> with <h4>
    for h2 in soup('h2'):
        h2.name = 'h4'

    #remove unnecessary attributes
    for tag in soup():
        for attribute in ['class', 'id', 'name', 'style']:
            del tag[attribute]
    
    #changes image path for KB site
    print(filename)
    filename = os.path.splitext(filename)[0]
    print(filename)
    for image in soup.findAll('img'):
        image['src'] = image['src'].replace(filename, "/images/group87/"+KBID)

    #self explanitory :)
    soup.prettify()

    #do string processing after here
    soup_string = str(soup)

    #removes all <p><br/></p> tags
    soup_string = soup_string.replace('<p><br/></p>', '')

    #encapsulates <p> tags in <body> with a <div>
    soup_string = soup_string.replace('<body>', '<body>\n<div>')
    soup_string = soup_string.replace('</body>', '</div>\n</body>')

    #exports file with .new at end
    with open(filepath+'.new', 'w') as file:
        file.write(str(soup_string))

    #preserves original html file (minus the dumb smart quotes) with a .old extension
    os.rename(filepath,filepath+'.old')
    os.rename(filepath+'.new', filepath)


if __name__ == "__main__":
    main()
