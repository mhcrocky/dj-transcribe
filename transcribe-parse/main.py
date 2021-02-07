"""Generate PDF from HTML."""
from pathlib import Path
import sys
import datetime
from weasyprint import HTML
import dominate
import json
from dominate.tags import *


def makepdf(html, base_url="assets"):
    """Generate a PDF file from a string of HTML."""
    htmldoc = HTML(string=html, base_url=base_url)
    return htmldoc.write_pdf()


def convertTimeZoneFromMiliSec(sec, isSrt=True):
    """ Make the timestamp such as 04:02:45 or 03:22:63, 893 """
    mainResult = str(int(sec / 1000 / 3600) + 100)[1:] + ":" + str(int(sec / 1000 / 60) + 100)[1:] + ":" + str(int(sec / 1000) % 60 + 100)[1:]
    if isSrt:
        return mainResult + "," + str(sec % 1000)
    else:
        return mainResult


def generateTxt(words, isTimeStamp=True, interVal=1, filename="output"):
    """Generate a Text file from JSON file"""
    """ Param1: outputed srt file name """
    """ Param2: words: the words obtained from json file """
    """ Param3: isTimeStamp: Enable/Disable to add timestamp into txt file """
    """ Param4: interVal: interval minute such as every 5 minutes, 2 minutes, 1 minutes(default: 1 minute)"""

    withFile = open("output/" + filename + ".txt", "w")
    if( isTimeStamp ):
        withFile.write("--00:00:00--\n")

    sentences = {}
    speaker = ""
    everycnt = 1

    for (ind, word) in enumerate(words):
        text = word['text']
        confidence = word['confidence']
        start = word['start']
        end = word['end']

        if isTimeStamp and start > everycnt * 1000 * 60 * interVal:
            everycnt = everycnt + 1
            resultStr = "\n-----------" + convertTimeZoneFromMiliSec(start, False) + "-----------\n"
            withFile.write(resultStr)

        if speaker != '' and speaker != word['speaker']:
            innerStr = "Speaker " + speaker + " : " + sentences[speaker] + "\n"
            withFile.write(innerStr)
            sentences[speaker] = ''

        speaker = word['speaker']

        if speaker in sentences:
            original = sentences[speaker]
        else:
            original = ''
        sentences.update({speaker: original + text + ' '})

    withFile.close()

def generatePDF(words, interVal=1, filename="output"):
    """Generate a PDF file from a string of HTML."""
    """ Param1: outputed srt file name """
    """ Param2: words: the words obtained from json file """
    """ Param3: interVal: interval minute such as every 5 minutes, 2 minutes, 1 minutes(default: 1 minute)"""
    doc = dominate.document(title='Transcription')
    with doc.head:
        link(rel='stylesheet', href='report.css')

    with doc:
        with article(id='cover'):
            h1('Transcription')
            address('https://www.youtube.com/watch?v=uRYcospQzzw')

    with doc:
        conthtml = article()
        conthtml.add(h2('00:00:00'))
        tblhtml = conthtml.add(table())


    sentences = {}
    speaker = ""
    everycnt = 1

    for (ind, word) in enumerate(words):
        text = word['text']
        confidence = word['confidence']
        start = word['start']
        end = word['end']

        if start > everycnt * 1000 * 60 * interVal:
            everycnt = everycnt + 1
            resultStr = f"\n{convertTimeZoneFromMiliSec(start, False)}\n"
            conthtml.add(h2(resultStr))
            tblhtml = conthtml.add(table())

        if speaker != '' and speaker != word['speaker']:
            speakerLeft = "Speaker " + speaker + "\n"
            speakerRight =  sentences[speaker] + "\n"
            tblhtml.add(tr([td(speakerLeft, id="left-col"), td(speakerRight, id="right-col")]))
            sentences[speaker] = ''

        speaker = word['speaker']

        if speaker in sentences:
            original = sentences[speaker]
        else:
            original = ''
        sentences.update({speaker: original + text + ' '})

        # conthtml.add(tblhtml)

    with open('assets/input.html', 'w') as f:
        f.write(doc.render())

    html = Path('assets/input.html').read_text()
    pdf = makepdf(html)
    Path('output/' + filename + '.pdf').write_bytes(pdf)

def generateSrt(words, filename="output"):
    """Generate a Srt file for video file."""
    """ Param1: outputed srt file name """
    """ Param2: words: the words obtained from json file """
    srtFile = open("output/" + filename + ".srt", "w")
    sentences = {}
    speaker = ""
    srtCnt = 1
    srt_startTime = 0
    srt_endTime = 0

    for (ind, word) in enumerate(words):
        text = word['text']
        confidence = word['confidence']
        start = word['start']
        end = word['end']
        if ind == 0:
            srt_startTime = start

        if speaker != '' and speaker != word['speaker']:
            if srtCnt != 1:
                srtFile.write("\n")
            srtFile.write(str(srtCnt) + "\n")
            srtFile.write(convertTimeZoneFromMiliSec(srt_startTime) + " --> " + convertTimeZoneFromMiliSec(srt_endTime) + "\n")
            srtFile.write(sentences[speaker] + "\n")
            srtCnt = srtCnt + 1
            srt_startTime = start
            sentences[speaker] = ''

        speaker = word['speaker']
        srt_endTime = end

        if speaker in sentences:
            original = sentences[speaker]
        else:
            original = ''
        sentences.update({speaker: original + text + ' '})

    srtFile.close()

def ParseJson(jsonPath):
    """return parsed Json from json file."""
    with open(jsonPath) as json_data:
        data = json.load(json_data)
    words = data['words']
    return words

def getRandomFileName():
    """get random file name with datetime."""
    current_time = datetime.datetime.now()
    resultFileName = str(current_time.hour) + "_" + str(current_time.minute) + "_" + str(current_time.second) + "_" + str(current_time.microsecond)
    return resultFileName

if __name__ == "__main__":
    jsonpath = "result.json"
    words = ParseJson(jsonpath)

    generateTxt(words, isTimeStamp=True, filename="output")
    generateTxt(words, isTimeStamp=False, filename="output-raw")
    generateSrt(words)
    generatePDF(words)

    print('Success: Results are stored in the output folder')
