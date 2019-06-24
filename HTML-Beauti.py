from bs4 import BeautifulSoup
import os, glob, sys

def file_replace_text(fname, toreplace, replacement):
    #print("opening " + fname)
    with open(fname, 'r',  encoding='utf-8') as file:
        filedata = file.read()
    # Replace the text in file
    filedata = filedata.replace(toreplace, replacement)
    # Write the file out again
    with open(fname, 'w', encoding='utf-8') as file:
        file.write(filedata)

def main():
    if len(sys.argv) <= 1:
        print("No parameters detected. Aborting.")
        input("Press Enter to continue...")
    elif len(sys.argv) == 1:
        #print("ARG detected: "+sys.argv[1])
        kbarg = sys.argv[1]
    else:
        kbarg = sys.argv[1:]

    #dirname = os.path.dirname(__file__)
    dirname = '\\\\FS-LS-2\\IT Department\\KB PDF2HTML\\Organized'
    # print(dirname)

    for KBID in kbarg:
        print('Beauti.pying ' + KBID, end=" ")
    
        folderpath = os.path.join(dirname, KBID)
        # print(folderpath)

        if not (os.path.isdir(folderpath)):
            print("KBID doesn't exist. Skipping...")
            continue

        # list all .html files in chosen directory (there should only be one)
        os.chdir(folderpath)
        for file in glob.glob('*.html'):
            filename = file
        os.chdir('..')

        filepath = os.path.join(folderpath, filename)

        #if .old version of file already, abort
        if os.path.exists(filepath+'.old'):
            print('File already converted. Skipping...')       #TODO: skip instead of abort
            continue

        print(filename, end=" ")

        #removing smart quotes
        file_replace_text(filepath, '“', '"')
        file_replace_text(filepath, '”', '"')
        file_replace_text(filepath, '’', '')
        #file_replace_text(filepath, '', '"')

        print(".", end=" ")

        #start html cleaning with beautifulsoup
        with open(filepath, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, "html.parser")

        print(".", end=" ")

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

        print(".", end=" ")
        
        #changes image path for KB site
        #print(filename)
        filename = os.path.splitext(filename)[0]
        #print(filename)
        for image in soup.findAll('img'):
            image['src'] = image['src'].replace(filename, "/images/group87/"+KBID)

        #self explanitory :)
        soup.prettify()

        #do string processing after here
        soup_string = str(soup.encode("utf-8"))

        print(".", end=" ")

        #removes all <p><br/></p> tags
        soup_string = soup_string.replace('<p><br/></p>', '')

        #encapsulates <p> tags in <body> with a <div>
        soup_string = soup_string.replace('<body>', '<body>\n<div>')
        soup_string = soup_string.replace('</body>', '</div>\n</body>')

        print(".", end=" ")

        #exports file with .new at end
        with open(filepath+'.new', 'w') as file:
            file.write(str(soup_string))

        #preserves original html file (minus the dumb smart quotes) with a .old extension
        os.rename(filepath,filepath+'.old')
        os.rename(filepath+'.new', filepath)

        print('done!')


if __name__ == "__main__":
    main()
