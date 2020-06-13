import flask,json
from flask import request, jsonify
import requests , datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def api_call():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    args = {'date' : today , 'sort' : 'stars' , 'order' : 'desc'}
    r = requests.get('https://api.github.com/search/repositories?q=created',params=args)
    return r.json()["items"]

#This function returns the number of repos using this language
@app.route('/get-number-of-repos',methods=['GET'])
def get_number_of_repos():
    repos = api_call()
    my_list_language = []
    for i in repos:
        my_list_language.append(i["language"])

    #Used to count the number of occurences of each language
    nb_repos_using_language = {i:my_list_language.count(i) for i in my_list_language}

    return json.dumps(nb_repos_using_language)


#This function returns the list of repos used by each language
@app.route('/get-repos',methods=['GET'])
def list_of_repos():
    repos = api_call()
    languages_dict = {} #Used to store the language as key and the list repos as values
    my_list_language = []

    for i in repos:
        my_list_language.append(i["language"])

    for i in set(my_list_language):
        repos_list = [] #For storing the repos using the same language
        for j in repos:
            if(j["language"]==i):
                repos_list.append(j["name"])
        languages_dict[i]=repos_list

    return json.dumps(languages_dict)
    
app.run()