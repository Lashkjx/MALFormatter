import json
import PySimpleGUI as sg
import pyperclip as clip

def getYears():
    years = []
    for i in range(35):
        years.append(2024 - i)
    return years

def getScores():
    scores = []
    for i in range(10):
        scores.append(1 + i)
    return scores

def get_seasonal(year):
    file = open('C:/Users/Kanan/Python/MAL Formatter/{}.json'.format(str(year)))
    seasonal = json.loads(file.read())
    return seasonal

def get_dropped():
    file_drop = open('C:/Users/Kanan/Python/MAL Formatter/Drop.json')
    seasonal_drop = json.loads(file_drop.read())
    return seasonal_drop

def get_hold():
    file_hold = open('C:/Users/Kanan/Python/MAL Formatter/Hold.json')
    seasonal_hold = json.loads(file_hold.read())
    return seasonal_hold

def get_medals():
    medals_file = open('C:/Users/Kanan/Python/MAL Formatter/Medals.json')
    optional_medals = json.loads(medals_file.read())
    return optional_medals

def get_scores(score):
    score_file = open('C:/Users/Kanan/Python/MAL Formatter/Scores.json')
    medal_score = json.loads(score_file.read())
    return medal_score[str(score)]
    
seasons = ['Winter', 'Spring', 'Summer', 'Fall']

status = ['Watching', 'Dropped']

sg.theme('DarkBlack')
frame_drop = [[sg.Checkbox('2010', key='drop_2010'), sg.Checkbox('2011', key='drop_2011'), sg.Checkbox('2012', key='drop_2012'), sg.Checkbox('2013', key='drop_2013'), sg.Checkbox('2014', key='drop_2014')],
              [sg.Checkbox('2015', key='drop_2015'), sg.Checkbox('2016', key='drop_2016'), sg.Checkbox('2017', key='drop_2017'), sg.Checkbox('2018', key='drop_2018'), sg.Checkbox('2019', key='drop_2019')],
              [sg.Checkbox('2020', key='drop_2020')]]
frame_hold = [[sg.Checkbox('2010', key='hold_2010'), sg.Checkbox('2011', key='hold_2011'), sg.Checkbox('2012', key='hold_2012'), sg.Checkbox('2013', key='hold_2013'), sg.Checkbox('2014', key='hold_2014')],
              [sg.Checkbox('2015', key='hold_2015'), sg.Checkbox('2016', key='hold_2016'), sg.Checkbox('2017', key='hold_2017'), sg.Checkbox('2018', key='hold_2018'), sg.Checkbox('2019', key='hold_2019')],
              [sg.Checkbox('2020', key='hold_2020')]]
frame_layaout = [[ sg.Text('Year:'), sg.Combo(values=getYears(), default_value='2020', size=(4,5), key='year'), sg.Text('Score:'), sg.Combo(values=getScores(), default_value=5, key='score'), sg.Text('Season:'), sg.Combo(values=seasons, default_value='Winter' ,key='season')],
                  [sg.Text(size=(3,1)), sg.Checkbox('Top', key='top'),sg.Checkbox('Shit', key='shit'), sg.Checkbox('AOTY', key='aoty'), sg.Checkbox('Best Girl', key='girl'), sg.Checkbox('Best Trap', key='trap') ]]
frame_optionals= [[ sg.Text('Optionals: '), sg.Checkbox('Idol hell', key='idol'), sg.Checkbox('Not Idol hell', key='noidol'), sg.Checkbox('Surprise', key='surprise'), sg.Checkbox('Food', key='food'), sg.Checkbox('Mahjong', key='mahjong')],
                  [ sg.Text(size=(8,1)), sg.Checkbox('Shoujo Ai', key='shoujo'), sg.Checkbox('Tear', key='tear'), sg.Checkbox('Cry', key='cry'), sg.Checkbox('Memes', key='memes'), sg.Checkbox('Romance', key='romance'), sg.Checkbox('Three Way', key='three')],
                  [ sg.Text(size=(8,1)), sg.Checkbox('3-D', key='3d'), sg.Checkbox('Animal', key='animal'), sg.Checkbox('Shounen', key='shounen'), sg.Checkbox('Spocon', key='spocon'), sg.Checkbox('Isekai', key='isekai'), sg.Checkbox('Ecchi', key='ecchi')],
                  [ sg.Text(size=(8,1)), sg.Checkbox('OP', key='op'), sg.Checkbox('ED', key='ed')]]
                 
layout = [  [sg.Text('Anime title: '), sg.InputText(key='title', size=(80,1)), sg.Checkbox('Dash', key='dash')],
            [sg.Text('  Start date:'),sg.InputText(size=(10,2), key='start'), sg.Text('End date:'),sg.InputText(size=(10,2),key='end'), sg.Checkbox('Disable dates', key='disabled')],
            [sg.Frame('Medals', frame_layaout)],
            [sg.Frame('Hold', frame_hold), sg.Frame('Drop', frame_drop)],
            [sg.Frame('Optionals', frame_optionals)],
            [sg.Text('BBCode: '), sg.Multiline(size=(80,3), key='bbcode')],
            [sg.Button('Ok'), sg.Button('Copy'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('MAL Formatter', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        break
    if event in (None, 'Copy'):
        clip.copy(values['bbcode'])
    seasonal_medals = get_seasonal(values['year'])
    season = get_seasonal(values['year'])
    medals = get_medals()
    drop = get_dropped()
    hold = get_hold()
    if values['dash'] == 0:
        bbcode = '[b]' + values['title'] + ' {}[/b]\n'
    else:
        bbcode = '[b] - ' + values['title'] + ' {}[/b]\n'
    if values['disabled'] == 0:
        if values['end'] is None:
            bbcode = bbcode.format(' [' + values['start'] + ' - ]')
        else:
            bbcode = bbcode.format(' [' + values['start'] + ' - ' + values['end'] + ']')
    else:
        bbcode = bbcode.format('')
    
    for value in values:
        if value == 'score':
            bbcode = bbcode + get_scores(values['score'])
        if value == 'season':
            bbcode = bbcode + season[values['season']]
        for i in range(11):
            drop_tag = 'drop_{}'
            if value == 'shit' and values[drop_tag.format(2010 + i)]:
                bbcode = bbcode + drop[str(2010 + i)]
        for e in range(11):
            hold_tag = 'hold_{}'
            if value == 'shit' and values[hold_tag.format(2010 + e)]:
                bbcode = bbcode + hold[str(2010 + e)]        
        if value == 'shit' and values['top'] == 1:
            bbcode = bbcode + medals['Top']
        if value == 'shit' and values['shit'] == 1:
            bbcode = bbcode + season['Shit']
        if value == 'shit' and values['aoty'] == 1:
            bbcode = bbcode + season['AOTY']
        if value == 'shit' and values['girl'] == 1:
            bbcode = bbcode + season['Girl']
        if value == 'shit' and values['trap'] == 1:
            bbcode = bbcode + season['Trap']
        if value == 'shit' and values['idol'] == 1:
            bbcode = bbcode + medals['Idol']
        if value == 'shit' and values['noidol'] == 1:
            bbcode = bbcode + medals['NoIdol']
        if value == 'shit' and values['surprise'] == 1:
            bbcode = bbcode + medals['Surprise']
        if value == 'shit' and values['food'] == 1:
            bbcode = bbcode + medals['Food']
        if value == 'shit' and values['mahjong'] == 1:
            bbcode = bbcode + medals['Mahjong']
        if value == 'shit' and values['shoujo'] == 1:
            bbcode = bbcode + medals['Shoujo']
        if value == 'shit' and values['tear'] == 1:
            bbcode = bbcode + medals['Tear']
        if value == 'shit' and values['cry'] == 1:
            bbcode = bbcode + medals['Cry']
        if value == 'shit' and values['memes'] == 1:
            bbcode = bbcode + medals['Memes']
        if value == 'shit' and values['romance'] == 1:
            bbcode = bbcode + medals['Romance']
        if value == 'shit' and values['three'] == 1:
            bbcode = bbcode + medals['Threeway']
        if value == 'shit' and values['3d'] == 1:
            bbcode = bbcode + medals['3D']
        if value == 'shit' and values['animal'] == 1:
            bbcode = bbcode + medals['Animal']
        if value == 'shit' and values['shounen'] == 1:
            bbcode = bbcode + medals['Shounen']
        if value == 'shit' and values['spocon'] == 1:
            bbcode = bbcode + medals['Spocon']
        if value == 'shit' and values['isekai'] == 1:
            bbcode = bbcode + medals['Isekai']
        if value == 'shit' and values['ecchi'] == 1:
            bbcode = bbcode + medals['Ecchi']
        if value == 'shit' and values['op'] == 1:
            bbcode = bbcode + medals['OP']
        if value == 'shit' and values['ed'] == 1:
            bbcode = bbcode + medals['ED']    
    window['bbcode'].update(bbcode)
    
window.close()