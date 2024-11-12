#import in order to call display function
from display_layout import display_layout
#import this in order to modify variable used in display function
from display_layout import current_layout

#this function switches layout on user input and calls display function
@app.route('/switch_layout', methods=['POST'])
def switch_layout():
    data = request.get_json() #info of whether the button was clicked or not by user
    if data.get('action') == 'clicked':
        global current_layout
        if current_layout == 'list_view':
            current_layout = 'calendar_view'
        elif current_layout == 'calendar_view':
            current_layout = 'list_view'
        else:
            print('Error occurred - unable to switch layout. Try again.') #if current layout is somehow not set to list_view
            current_layout = 'list_view' #reset layout to default view
        display_layout(current_layout)
    else:
        pass #button not clicked, do nothing
