import sys, os
import xml.etree.ElementTree as ET
import webify

#needs one argument -- the directory with the docs
directory = os.fsencode(sys.argv[1])

def parse_test(location, num):
    #html file for web page
    html_text = ''

    #parse document
    try:
        mytree = ET.parse(location)
        root = mytree.getroot()
        id = root.attrib['identifier']
    except Exception as e:
        print('.....error parsing file......')
        print(e)
    else:
        html_text += str(num)
        html_text += webify.single('ID', id)
        html_text += get_question(root, id )
        html_text += correct_response(root, id)
        html_text += student_choices(root, id)
        html_text += give_feedback(root, id)
        html_text += '<hr>'
    return html_text

def get_question(root, id):
    #get question # and question
    try:
        question = root.attrib['title']
    except Exception as e:
        print('problem with get question for doc: ' + id)
        print(e)
    return webify.single('Question', question)

def correct_response(root, id):
    response = []
    try:
        for x in root.findall('responseDeclaration/correctResponse'):
            for y in iter(x):
                if y.tag == 'value':
                    response.append(y.text)
    except Exception as e:
        print('problem with response for doc: ' + id)
        print(e)

    return webify.multiple('Correct Responses', response)

def student_choices(root, id):
    response = []
    try:
        for x in root.findall('itemBody/choiceInteraction'):
            for y in iter(x):
                if y.tag == 'simpleChoice':
                    response.append(y.attrib['identifier'] + '--> ' + y.text)
    except Exception as e:
        print('problem with student choices' + id)
        print(e)
    else:
        return webify.multiple('Student Choices', response)

def give_feedback(root, id):
    try:
        for x in root.findall('modalFeedback'):
            for y in iter(x):
                if x.attrib['identifier'] == 'CORRECT_FEEDBACK':
                    feedback = y.text
    except Exception as e:
        print('problem with feedback' + id)
        print(e)
    else:
        return webify.single('Feedback', feedback)



if __name__ == '__main__':

    html = ''
    num = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.xml'):
            test_location = os.path.join(directory, file)
            print('parsing ' + filename)
            html += parse_test(test_location, num)
            num += 1

    with open('test.html', 'w') as fout:
        fout.write(html)

