def single(title, content):
    text = '<h2>' + title + '</h2>'
    text += '<p>' + content + '</p>'
    return text

def multiple(title, content):
    text = '<h2>' + title + '</h2>'
    text += '<ul>'
    for x in content:
        text += '<li> ' + x + '</li>'
    text += '</ul>'
    return text
