import networkx as nx
from bs4 import BeautifulSoup
import os
import tempfile
import numpy as np
import pylab as plt

text = []
array = []
j, i = 0, 0
sudopass = 'grakachak94'   #Your sudo password to create temporary files
temp_out = tempfile.NamedTemporaryFile()
tempfile.tempdir = "/home/paul/Biocad"

Entities = []

def PMparser():

#A function that parses text from a bunch of articles in xml

    with open("/home/paul/Biocad/pubmed_example.xml") as source:
        source = BeautifulSoup(source, features='lxml')
        global text
        text = source.find_all('abstracttext')
        return(text)

def SemRep(t):

#A function that recieves a text of single abstract as an input, invokes SemRep, writes the SemRep output to a temporary xml file, and returns a number of processed article

    global j
    j += 1
    temp_in = open('/home/paul/Biocad/input_' + str(j), 'w+', encoding='utf-8')
    temp_in.write(t.get_text()+ '\n')
    temp_in.close()
    temp_out = ' /home/paul/Biocad/xml/' + str(j)
    command = 'sudo bash /etc/MetaMap/public_semrep/bin/semrep.v1.8 ' + '/home/paul/Biocad/input_' + str(j) + temp_out + ' -X'
    os.system('echo %s|sudo -S %s' % (sudopass, command))
    os.remove('/home/paul/Biocad/input_' + str(j))
    return j

def Abs2Arr(source):

#A function that converts SemRep xml-results to a numpy array, suitable for graphs building

    global array
    
    source = BeautifulSoup(source, features='lxml')
    e = source.find_all('entity')
    for l in e:
        Entities.append((l.get('id'), l.get('name')))

    r = source.find_all('predication')
    for q in r:

        global G
        G = nx.Graph()

        subject = q.find('subject')
        object = q.find('object')
        predicate = q.find('predicate')

        sub_type = subject.get('relsemtype')
        obj_type = object.get('relsemtype')

        #making an array, looking like [(subject, subject_type, object, object_type, predicate)]
        array.append((j, [x[1] for x in Entities if str(x[0]) == str(subject.get('entityid'))][0], sub_type, [x[1] for x in Entities if str(x[0]) == str(object.get('entityid'))][0], obj_type, predicate.get('type')))

        try:
            os.remove('/home/paul/Biocad/xml/' + str(j))
        except Exception:
            continue


PMparser()
for t in text:
    SemRep(t)
    source = open('/home/paul/Biocad/xml/' + str(j))
    Abs2Arr(source)

num_arr = np.array(array)
np.save('/home/paul/Biocad/GraphArray.npy', num_arr)

#loading and preprocessing a numpy array for graphs

GraphsArray = np.load('/home/paul/Biocad/GraphArray.npy')
supergraph = nx.Graph()
G = nx.MultiGraph()

weight = 0


WeightArray = np.ones((GraphsArray.shape[0], 1)) #Here is a temporary patch - I forgot to add weight in array while creating it in Abs2Arr, so I add this element to each row of the array two rows lower
enumerateArray = np.arange(GraphsArray.shape[0]) #Another temporary solution - I forgot to enumerate the rows in the array, so I made it here, three rows lower

new = np.append(GraphsArray, WeightArray, axis=1)
new = np.insert(new, 0, enumerateArray, axis=1)
r = []

for i in new:
    for j in new:
        if i[0] != j[0] and i[2] == j[2] and i[2] != None and j[2] != None:  #Check whether out subject are identical
            if i[4] == j[4] and i[6] == j[6]:   #Check whether both objects and relations are identical
                i[7] += 1   #If so, adding weight
        if i[0] != j[0] and i[1] == j[1] and i[2] == j[2] and i[3] == j[3] and i[4] == j[4] and i[5] == j[5] and i[6] == j[6]:   #Finding full duplicates
            r.append(i[0])   #Append number of duplicating rows to "cleanup list"
            r.append(j[0])
        if i[2] == None or i[4] == None:   #Finding nonsence objects and subjects
            r.append(i[0])   #Append number of such rows to "cleanup list"


r = list(set(r))

unique = np.delete(new, r, axis=0)   #Cleaning up unnessesary rows

unique_subj = list(set(np.ndarray.tolist(unique[:,2])))   #Making a list of unique subjects

supermatrix = []

#building graphs
for x in unique_subj:   #For each unique subject we look at the rows of our array. If subject in a row of the array is equil to the unique subject, we add the row to another array. Then we add this array to superarray
                        #By this operation we recieve a superarray, which consists of arrays groupped by subject
    matrix = np.zeros((1,8))   #Empty array won't work for some reasons, so I made a zero-based array and "cut" the first zero row later
    for y in unique:

        if y[2] == x:
            matrix = np.vstack((matrix, y))
    supermatrix.append(matrix[1:])   #Here I append an inner sub-array with one subject to a superarray. Note, that superarray is LIST now, NOT NUMPY ARRAY!

supermatrix = np.array(supermatrix)   #Converting list to numpy array
'''A "superarray" groupped by subject looking like [[[number, number of article, subject_1, sub_type, obj_1, obj_type, relation, weight],
                                                     [number, number of article, subject_1, sub_type, obj_2, obj_type, relation, weight],
                                                     [number, number of article, subject_1, sub_type, obj_3, obj_type, relation, weight]],
                                
                                                    [[number, number of article, subject_2, sub_type, obj_1, obj_type, relation, weight],
                                                     [number, number of article, subject_2, sub_type, obj_2, obj_type, relation, weight]]...'''

count = 1

for i in supermatrix:   #Iterating over inner sub-arrays

    G.add_nodes_from(i[:,2], type=i[:,3])   #Adding node from subject of a sub-array. Subject is identical for all rows of the sub-array, so we can just use G.add_node(i[2]). Hope that we have a single subject node with a list of possible types here

    for j in i:   #Iterating over rows in sub-array
        G.add_node(j[4], type=j[5])    #All subjects, which are i[2], are identical, so we just add another node for each object (j[4]) along with its type
        if j[4] not in str(G.edges.data()):    #If there is no edge between our subject (i[2]) and object (j[4)] we add it
            G.add_edge(list(G.nodes)[0], list(G.nodes)[-1], relation=j[6], weight=j[7])

    edge_labels = nx.get_edge_attributes(G, 'relation')
    plt.figure(figsize=(10,10))
    nx.draw_networkx(G)
    pos = nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G, pos=pos, labels=edge_labels, font_size=8)
    plt.savefig('/home/paul/Biocad/graphs/graph'+str(count)+'.png')
    plt.clf()
    plt.close()

    count+=1
    G.clear()   #After saving a PNG we clear the graph. I think it will be cool to add this graph as a node to "supergraph", which will represent the structure of the article: Node_1 = title, Node_2 = abstract etc.
