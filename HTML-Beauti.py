from bs4 import BeautifulSoup










def file_replace_rext(filename, toreplace, replacement):
    with open(filename, 'r',  encoding='utf-8') as file:
        filedata = file.read()
    # Replace the text in file
    filedata = filedata.replace(toreplace, replacement)
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)

# Read in the file
with open('todo.html', 'r',  encoding='utf-8') as file:
  filedata = file.read()
# Replace the “smart quotes”
filedata = filedata.replace('“', '"').replace('”', '"')
# Write the file out again
with open('todo.html', 'w') as file:
  file.write(filedata)

#TODO: verify if removing entire style tag is good or no


with open("todo.html", encoding='utf-8') as fp:
    soup = BeautifulSoup(fp, "html.parser")


title = soup.title.get_text()
print(title)

#remove style tag from header
soup.find('style').extract()

for tag in soup():
    for attribute in ['class', 'id', 'name', 'style']:
        del tag[attribute]

#do string processing after here
soup_string = str(soup)

#removes all <p><br/></p> tags
soup_string = soup_string.replace('<p><br/></p>', '<br/>')

#encapsulates <p> tags in <body> with a <div>
soup_string = soup_string.replace('<body>', '<body>\n<div>')
soup_string = soup_string.replace('</body>', '</div>\n</body>')

#exports file
with open('done.html', 'w') as file:
    file.write(str(soup_string))
