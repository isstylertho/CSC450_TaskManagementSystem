#MOVED THIS INTO CSC 450 CODE.PY

#this defines the layout to display list view by default
current_layout = 'list_view'

#this function checks the active layout and displays it
def display_layout():
    global current_layout
    if current_layout == 'list_view':
        #insert command to display list view layout (may need connected to Flask)
        print('list_view is being displayed')
    elif current_layout == 'calendar_view':
        #insert command to display calendar view layout (may need connected to Flask)
        print('calendar_view is being displayed')
    else:
        print('There was an issue displaying the layout. Try again.')
    
