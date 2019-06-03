from bottle import run, route, view, get, post, request, template, static_file #Import important bottle methods
from datetime import * #Import date time

###Classes###
class Bro: #Bro class
    def __init__(self, name, description, img, cost, stock, booked_details=""): #Constructor
        #Set bro personal variables
        self.name = name
        self.description = description
        self.img = img
        self.stock = stock
        self.cost = cost
        self.booked_details = booked_details
       

###Arrays###     
MONTHS = { #List of months with their numbers to help convert the dates on purchase success page
    'Jan' : 1,
    'Feb' : 2,
    'Mar' : 3,
    'Apr' : 4,
    'May' : 5,
    'Jun' : 6,
    'Jul' : 7,
    'Aug' : 8,
    'Sep' : 9, 
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12
}
        
bros = [ #Test data filled with test bros
    Bro("Tom","Generic british boi. Nice and smart so don't hire him if you don't want to feel bad about your IQ. Will colonise only if it brings glory to his queen.","tom.jpg", 970, True),
    Bro("Jerry","Good boi, will definatly tell us everything you did wrong. Cops might like this one.","jerry.jpg", 90, True),
    Bro("Moses","Slightly retarded, will do anything for you. Makes you feel better about your problems. Depressed people and bullies may want.", "moses.jpg", 20, True),
    Bro("John","Goes to the gym.","john.jpg", 100, True),
    Bro("Liam","Will serinade. Has guitar, good boi. Ideal for girls.","liam.jpg", 100, True),
    Bro("Fox","Will sit and play nintendo with you for as long as you like. Presence makes you feel good. Introvertes love.","laimf.jpg", 78, True),
    Bro("Dom","Will make you feel geneticaly inferior. Has good beauty products. Gays would buy again.","dom.jpg", 20, False)
]

###Pages###
#Index page
@route('/')
@view('index')
def index():
    pass

#Product page
@route('/products.html')
@view('products.html')
def products():
    return dict(bros_list = bros)

#Purchase page
current_bro = None #This variable is used to easily pass the currently processed bro through pages, (Purchase -> purchase success page)
@route('/purchase/<name>')
@view('purchase')
def purchase(name):
    global current_bro
    #Find the bro by name
    found_bro = None
    for bro in bros:
        if name == bro.name:
            found_bro = bro
            break
    found_bro.stock = False
    current_bro = found_bro #Set the object as current bro and return it to the page
    return dict(bro = found_bro) #Return found_bro to page

#Purchase_success page
@route('/purchase_success', method = "POST")
@view('purchase_success')
def purchase_success():
    #Get form data entries
    Fname = request.forms.get("first_name")
    Lname = request.forms.get("last_name")
    date_ = request.forms.get("date") #(Format i think is (Month(first 3 characters) dd, yyyy)
    
    #Format the date
    date_alt = date_.split(" ")
    date_alt[1] = date_alt[1].strip(",")
    
    #Calculate the difference in date and then the total cost
    curr_date = datetime.now()
    d0 = date(curr_date.year, curr_date.month, curr_date.day)
    d1 = date(int(date_alt[2]), int(MONTHS[date_alt[0]]), int(date_alt[1]))
    delta = d1 - d0
    
    if delta * -1 == abs(delta): #If user selected a past date then make the year go up by one
        d0 = date(curr_date.year, curr_date.month, curr_date.day)
        d1 = date(int(date_alt[2]) + 1, int(MONTHS[date_alt[0]]), int(date_alt[1]))
        delta = d1 - d0        
        
    total_cost = current_bro.cost * min(delta.days, 1)
    total_cost = str(total_cost)
    current_bro.stock = False #Change stock
    current_bro.booked_details = [Fname, Lname, str(curr_date.strftime("%B")) + " " + str(curr_date.day) + ", " + str(curr_date.year), date_, total_cost] #Store the booked details in the object
    return dict(bro = current_bro) #Pass object back into page


##Static files###
#Images
@route('/img/<filename>')
def server_static(filename):
    return static_file(filename, root='./Images')
#Css files
@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./Css')
#Script files
@route('/script/<filename>')
def server_static(filename):
    return static_file(filename, root='./Script')

run(host='0.0.0.0', port = 399, reloader = True, debug = True) #Run local server