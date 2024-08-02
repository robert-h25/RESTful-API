# client script to test the commands for the news api
import requests

#global variable for username and password
username = None
password = None

#global session
session = requests.Session()

#base_url change when we have deployed
base_url = "https://sc21rh.pythonanywhere.com"

def login(command):
    global username, password
    command_url = command.split()

    # Check if both command and url are provided
    if len(command_url) == 2:
        command, url = command_url
                    
        print("Enter the username and password")
        temp_username = input("Enter Username: ")
        temp_password = input("Enter Password: ")
        #send to url with user data
        response = session.post(url, data={"username": temp_username, "password": temp_password})   
        #check response code
        if response.status_code == 200:
            print("Success!")
            # set username and password
            username = temp_username
            password = temp_password
        else:
            print("Failed to send response status code:", response.status_code)             
    else:
        print("Incorrect argument count. Use login url")
        
    return

def logout():
    # check we have session id 
    if(not 'sessionid' in session.cookies):
        print("Please login first with: login url")
        return
        
    url = f"{base_url}/api/logout"
    session.auth = (username,password)
    response = session.post(url)
    #check response
    if response.status_code == 200:
            print("Success!")
    else:
        print("Failed to send response status code:", response.status_code)
    return

def post():
    # check we have session id 
    if(not 'sessionid' in session.cookies):
        print("Please login first with: login url")
        return
    print("Enter the story’s headline, category, region, and details")            
    headline = input("Headline: ")
    story_cat = input("Category: ")
    region = input("Region: ")
    details = input("Details: ")

    # authenticate username and password
    session.auth = (username,password)
    # Create json object
    url = f"{base_url}/api/stories"
    headers = {'Content-Type': 'application/json'}  
    json_data = {'headline':headline,'category':story_cat,'region':region,'details':details}  

    response = session.post(url, json=json_data, headers=headers)

    #check response
    if response.status_code == 200:
            print("Success!")
    else:
        print("Failed to send response status code:", response.status_code)
    return

def news(command):
    # check we have session id 
    if(not 'sessionid' in session.cookies):
        print("Please login first with: login url")
        return
        
    #default parameters are None
    service_id = None
    category = None
    region = None
    date = None
    command_key = command.split(maxsplit=1)
    # if we have parameters
    if len(command_key) > 1:
        parameters = command_key[1:]

        for arguments in parameters:
            if arguments.startswith("-id="):
                service_id = arguments.split("=")[1]
            elif arguments.startswith("-cat="):
                category = arguments.split("=")[1]
            elif arguments.startswith("-reg="):
                region = arguments.split("=")[1]
            elif arguments.startswith("-date="):
                date = arguments.split("=")[1]
    else:
        pass
    
    #default values if news tags are blank
    if not service_id:
        service_id = "*"
    if not category:
        category = "*"
    if not region:
        region = "*"
    if not date:
        date = "*"        

    #create json object
    url = f"{base_url}/api/stories"
    session.auth = (username,password)
    headers = {'Content-Type': 'application/json'}  
    data = {'story_cat':category,'story_region':region,'story_date':date,'id':service_id}  
    # send request to server
    response = session.get(url, data=data, headers=headers)
        
    if response.status_code == 200:
            print("Success!")
            # get json object 
            data = response.json()
            stories = data['stories']
            # for each story extract variables
            for story in stories:
                story_key = story['key']
                headline = story['headline']
                story_category = story['story_cat']
                story_region = story['story_region']
                author = story['author']
                story_date = story['story_date']
                story_details = story['story_details']
                print("Key:", story_key)
                print("Headline:", headline)
                print("Category:", story_category)
                print("Region:", story_region)
                print("Author:", author)
                print("Date:", story_date)
                print("Details:", story_details,"\n")
        
    else:
        print("Failed to send response status code:", response.status_code)  
    return

def list():
    # Send Get request to the server
    url =  "http://newssites.pythonanywhere.com/api/directory/" 
    response = requests.get(url) 
    if response.status_code == 200:
        # get json object
        data = response.json()
        # get agency_name,url and agency_code for each agency
        for agency in data[:20]:
            agency_name = agency['agency_name']
            agency_url = agency['url']
            agency_code = agency['agency_code']
            print("Agency Name: ", agency_name)
            print("URL: ", agency_url)
            print("Agency Code: ", agency_code)
        
    else:                
        # process errors
        print("Failed to send response status code:", response.status_code) 
    return

def delete(command):
    # check we have session id 
    if(not 'sessionid' in session.cookies):
        print("Please login first with: login url")
        return
        
    command_key = command.split()

    # Check if both command and key are provided
    if len(command_key) == 2:
        command, key = command_key
    else:
        print("Error: expected command = delete story_key")
    session.auth = (username,password)
    url = f"{base_url}/api/stories/{key}"
    response = session.delete(url) 
    # check response code   
    if response.status_code == 200:
            print("Success!")
    else:
        print("Failed to send response status code:", response.status_code) 
    return

def client():
    #set username and password as global variables
    global username, password

    while True:
        #get command
        command = input("Enter your command: ")
        #set base url
        base_url = "http://127.0.0.1:8000"
        

        # figure out what command it is
        if command.split()[0] == "login":
            login(command)
            
        elif command == "logout":
            logout()

        elif command == "post":
            post()                   

        elif command.split()[0] == "news":
            news(command)
                       
            
        elif command == "list":
            list()
                    

        elif command.split()[0] == "delete":
            delete(command)
        
        elif command == "stop":
            print("Goodbye!")
            return
        
        else:
            print("Incorrect command")


if __name__ == "__main__":
    client()