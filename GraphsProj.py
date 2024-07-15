import random
import pygame
import time

#declare global variables
num_nodes = 0
num_edges = 0
vertices = []
edges = []
dfs_all_paths = []

#use this variable to keep track of the sleeps we use that make the animation look good
bfs_time_added = 0

#We create an instance of a color object to make it easier to se with pygame components#
class Color():
    '''make a color class for more readable testing and debugging'''
    def __init__(self, color, three_nums):
        '''make a color thats a string for readability and the three_nums for using'''
        self.color = color
        self.three_nums = three_nums

#We create an object instance of nodes, so we can give it various conditions that can differ for each graph and node#
class Node():
    def __init__(self, x_coord, y_coord, radius, letter, color, font_color, bfs_distance, bfs_parent, bds_source_parent, bds_dest_parent):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.radius = radius
        self.letter = letter
        self.color = color
        self.font_color = font_color
        self.bfs_distance = bfs_distance
        self.bfs_parent = bfs_parent
        self.bds_source_parent = bds_source_parent
        self.bds_dest_parent = bds_dest_parent

#We create an object for each instance of an edge, which makes it easier to draw and gives it conditions that vary per edge#
class Edge():
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

#We generate the graph at first, so we can draw it and create a basis to come back to for each graph traversal algorithm#
def graphGeneration():
    #this function is going to randomly generate the graph
    #lets start by determining the number of nodes
    global num_nodes 
    global num_edges
    global vertices
    global edges
    num_nodes = (int)(random.randint(3,8))

    temp_edges = [] # used for seeing if there's duplicates

    #now lets get the number of edges
    max_num_edges = (int)(num_nodes)*(num_nodes-1)/2
    num_edges = (int)(random.randint(2,max_num_edges))

    #make the list of vertices
    for i in range(num_nodes):
        #A is 65, so count up from there
        vertices.append(Node(0,0,30,chr(i+65),Color('black',(0,0,0)),Color('black',(0,0,0)), float('inf'), -1, -1, -1))

    #make the list of edges 
    while(len(edges) < num_edges):
        item1 = random.choice(vertices)
        item2 = random.choice(vertices)
        one_edge = set()

        #make sure we don't do an edge to ourself
        while(item2.letter == item1.letter):
            item2 = random.choice(vertices)

        one_edge = {item1.letter,item2.letter}

        #make sure the edge doesn't already exist
        if(not (one_edge in temp_edges)):
            temp_edges.append(one_edge)
            edges.append(Edge(item1, item2))
    
#We create the initial positions for each node, modifying the conditions in the class and making it easy to draw#
def makeNodePositions():
    global num_nodes
    global num_edges
    global vertices

    for i in range(num_nodes):
        #make some specific positions for readability
        if (i==0):
            x=250
            y=100
        elif(i==1):
            x=750
            y=100
        elif(i == 2):
            y=275
            x=500
        elif(i==3):
            x=125
            y=400
        elif(i==4):
            x=875
            y=400
        elif(i == 5):
            y=525
            x=500
        elif(i==6):
            x=250
            y=700
        else:
            x=750
            y=700
        vertices[i].x_coord = x
        vertices[i].y_coord = y
        vertices[i].color = color_white
        vertices[i].radius = 40
        vertices[i].font_color = color_black

#We draw each node on the graph, we can do this after updating the color for the visual representations#
def drawNodes():
    global num_nodes
    global vertices

    for vertex in vertices:
        pygame.draw.circle(screen, vertex.color.three_nums, (vertex.x_coord,vertex.y_coord), vertex.radius) #for the color fill
        pygame.draw.circle(screen, color_black.three_nums, (vertex.x_coord,vertex.y_coord), vertex.radius, 4) #for the outline

        #to write each letter
        letter_text = pygame.font.Font('freesansbold.ttf',26).render(vertex.letter, True, vertex.font_color.three_nums)
        screen.blit(letter_text, (vertex.x_coord-9, vertex.y_coord-11)) #use these numbers to center it

#We draw each edge on the graph, based on the node locations and drawn for the visual representation#
def drawEdges():
    global edges

    for edge in edges:
        pygame.draw.line(screen, color_black.three_nums, (edge.start_node.x_coord, edge.start_node.y_coord), (edge.end_node.x_coord, edge.end_node.y_coord), 2)

#This is our graphical representation of BFS, but it also functions for our shortest path algorithm#
def BFS(vertices, edges, source_vertex):
    global bfs_time_added
    #we start by going to the first node
    source_vertex.color = color_gray
    update_time = time.time()
    drawNodes()
    pygame.display.flip()
    update_time = time.time()-update_time
    time.sleep(.5)
    bfs_time_added += 0.5
    bfs_time_added += update_time

    #add our first vertex to the visited queue
    vertices_queue = []
    source_vertex.bfs_distance = 0 
    vertices_queue.append(source_vertex)

    while (len(vertices_queue) > 0):

        #dequeue the vertex in the queue
        current_vertex = vertices_queue.pop(0)

        #make adjacency set rq
        adj_v = set()
        for edge in edges:
            if(edge.start_node.letter == current_vertex.letter):
                adj_v.add(edge.end_node)

            elif (edge.end_node.letter == current_vertex.letter):
                adj_v.add(edge.start_node)

        #time to go through all of these edges
        for node in adj_v:
            #check if unvisited
            if (node.color.color == 'white'):
                #change it to gray
                node.color = color_gray

                #mark the parent so we can get the shortest path
                node.bfs_parent = current_vertex

                #set the distance as the current node's plus 1
                node.bfs_distance = current_vertex.bfs_distance+1

                #queue up the edgy end node
                vertices_queue.append(node)

        #update all nodes that flipped to be gray
        update_time = time.time()
        drawEdges()
        drawNodes()
        pygame.display.flip()
        update_time= time.time()-update_time
        time.sleep(1)
        bfs_time_added +=1
        bfs_time_added += update_time

        current_vertex.color = color_black
        current_vertex.font_color = color_white

        update_time= time.time()
        drawEdges()
        drawNodes()
        pygame.display.flip()
        update_time = time.time()-update_time
        time.sleep(.5)
        bfs_time_added+=.5
        bfs_time_added+=update_time

        #ALSO USED FOR FINDING ALL DISCONNECTED NODES

        # #update while loop condition
        # #use a var to track whether or not all then nodes are black
        # count_black = 0
        # for v in vertices:
        #     if (v.color.color == 'black'):
        #         #if node is black, append to the count
        #         count_black+=1
        # #check if all nodes are black - if they are, we are done iterating through
        # if(count_black == len(vertices)):
        #     not_all_black = False

#This is the algorithm that finds the shortest path using modified BFS#
def BFS_shortest_path(vertices, edges, source_vertex, destination_vertex):
    global bfs_time_added
    bfs_time_added = 0
    #make our call to BFS
    BFS(vertices, edges, source_vertex)

    #check if the source and destination are connected
    if(destination_vertex.bfs_distance == float('inf')):
        return -10
    
    shortest_path = []
    current_vertex = destination_vertex

    shortest_path.append(destination_vertex)

    #get the shortest path by iterating through the path from the destination to the source
    while(current_vertex.bfs_parent != -1):
        shortest_path.append(current_vertex.bfs_parent)
        #move to the next node
        current_vertex = current_vertex.bfs_parent
    
    return shortest_path    
    
#This is the graphical representation of our DFS algorithm#
def DFS(vertices, edges):
    #gotta reset everything after BFS
    for v in vertices:
        v.color = color_white
        v.font_color = color_black
        
    drawEdges()
    drawNodes()
    pygame.display.flip()

    for v in vertices:
        if (v.color.color == 'white'):
            DFS_Visit(v, edges)

#This is our recursive call for the graphical representation of DFS#
def DFS_Visit(vertex, edges):
    vertex.color = color_gray

    drawEdges()
    drawNodes()
    pygame.display.flip()
    time.sleep(1)

    #make the adjacency set
    adj_v = set()
    for edge in edges:
        if(edge.start_node.letter == vertex.letter):
            adj_v.add(edge.end_node)

        elif (edge.end_node.letter == vertex.letter):
            adj_v.add(edge.start_node)

    #iterate thru edges
    for node in adj_v:
        if (node.color.color =='white'):
            DFS_Visit(node, edges)

    vertex.color = color_black
    vertex.font_color = color_white

    drawEdges()
    drawNodes()
    pygame.display.flip()
    time.sleep(1)

#This algorithm is separate from the graphical DFS, and returns all of the paths found from the source to the destination#
def DFS_shortest_path(source_vertex, destination_vertex, visited_letters, path_letters):
    global dfs_all_paths
    #now, if the current vertex the same as destination, print the current path
    if (source_vertex.letter == destination_vertex.letter):
        for let in path_letters:
            dfs_all_paths.append(let)
        return

    #need to get adjacency set
    adj_v = set()
    for edge in edges:
        if(edge.start_node.letter == source_vertex.letter):
            adj_v.add(edge.end_node)
        elif (edge.end_node.letter == source_vertex.letter):
            adj_v.add(edge.start_node)
    
    #add our source to the visited list and our path
    visited_letters.append(source_vertex.letter)

    #them, for every adjacent node, recursively run this dfs on it again
    for node in adj_v:
        #if it is unvisited, we perform the same thing on  it
        if(node.letter not in visited_letters):
            path_letters.append(node.letter)
            DFS_shortest_path(node, destination_vertex, visited_letters, path_letters)
            path_letters.remove(node.letter)
    #when done, that means all the nodes have been visited
    visited_letters.remove(source_vertex.letter)

#This sets all of our basis variables to make changes to in the DFS shortest_path function#
def all_DFS_paths(source_vertex, destination_vertex):
    global dfs_all_paths
    dfs_all_paths = []
    visited_letters = []
    path_letters = []
    path_letters.append(source_vertex.letter)

    DFS_shortest_path(source_vertex, destination_vertex, visited_letters, path_letters)

#This is our application of BFS for BDS from the source to the destination#
def BDS_BFS_forward(source_queue, source_visited_letters):
    current_vertex = source_queue.pop(0)

    #get the adjacency set
    adj_v = set()
    for edge in edges:
        if(edge.start_node.letter == current_vertex.letter):
            adj_v.add(edge.end_node)

        elif (edge.end_node.letter == current_vertex.letter):
            adj_v.add(edge.start_node)

    for v in adj_v:
        if (v.letter not in source_visited_letters):
            source_queue.append(v)
            source_visited_letters.append(v.letter)
            v.bds_source_parent = current_vertex

#This is our applcation of BFS for BDS from the destination to the source#
            #We need two based on the parents that get switched
def BDS_BFS_backward(dest_queue, dest_visited_letters):
    current_vertex = dest_queue.pop(0)

    #get the adjacency set
    adj_v = set()
    for edge in edges:
        if(edge.start_node.letter == current_vertex.letter):
            adj_v.add(edge.end_node)

        elif (edge.end_node.letter == current_vertex.letter):
            adj_v.add(edge.start_node)

    for v in adj_v:
        if (v.letter not in dest_visited_letters):
            dest_queue.append(v)
            dest_visited_letters.append(v.letter)
            v.bds_dest_parent = current_vertex

#This checks whether or not the paths intersect based on the two BFSs for our BDS algorithm#
def BDS_check_intersect(source_letters, destination_letters):
    for v in vertices:
        if (v.letter in source_letters and v.letter in destination_letters):
            return v
            
    #if no nodes intersect, then they are disconnected
    return -1
        
#This returns the shortest path for our BDS algorithm#
def BDS_get_path(intersecting_node, source_vertex, destination_vertex):
    path = []
    path.append(intersecting_node)
    current_vertex = intersecting_node

    #get the path for the source vertex
    while (current_vertex.letter != source_vertex.letter):
        path.append(current_vertex.bds_source_parent)
        current_vertex = current_vertex.bds_source_parent

    path = path[::-1]
    #do the same thing for the destination path
    current_vertex = intersecting_node

    while(current_vertex.letter != destination_vertex.letter):
        path.append(current_vertex.bds_dest_parent)
        current_vertex = current_vertex.bds_dest_parent

    letter_path = []
    for elem in path:
        letter_path.append(elem.letter)
    
    return letter_path

#We use this function to facilitate the use of all of our other BDS functions. Primarily, returns the shortest path for BDS#
def BiDirectional_Search(source_vertex, destination_vertex):
    source_queue = []
    source_visited_letters = []
    destination_queue = []
    destination_visited_letters = []

    #make the start of the queues on each side
    source_queue.append(source_vertex)
    source_visited_letters.append(source_vertex.letter)


    destination_queue.append(destination_vertex)
    destination_visited_letters.append(destination_vertex.letter)


    while (len(source_queue) > 0 and len(destination_queue) > 0):
        #do BFS on the source node
        BDS_BFS_forward(source_queue, source_visited_letters)
        
        #then do it again on the destination node
        BDS_BFS_backward(destination_queue, destination_visited_letters)

        intersected_node = BDS_check_intersect(source_visited_letters, destination_visited_letters)

        if (intersected_node != -1):
            #if there is an intersecting node, print the path
            path = BDS_get_path(intersected_node, source_vertex, destination_vertex)
            break

    if(intersected_node == -1):
        return -1
    else:
        return path
    
if __name__ == "__main__":
    graphGeneration()
    pygame.init()
    #screen/window variables
    screen_width = 1000
    screen_height = 900
    screen = pygame.display.set_mode([screen_width,screen_height])
    game_frames_per_second = 60
    #use pygame's built in timer so I can edit when things happen
    timer = pygame.time.Clock()

    #set up out constant color variables so we can use them when drawing and changing nodes
    color_white = Color('white',(255,255,255))
    color_black = Color('black',(0,0,0))
    color_gray = Color('gray',(128,128,128))
    color_light_blue = Color('light blue',(173,216,230))

    #make the positions of the nodes for when we draw them within the game loop
    makeNodePositions()

    #get which nodes you would like to start and end at
    source_node = vertices[0]
    destination_node = vertices[len(vertices)-1]

    #make boolean variables to control which graph traversal algorithm is being run
    DFS_done = False
    BFS_done = False
    BDS_done = False

    is_game_running = True
    while(is_game_running):
        #get a fps ticker and fill the screen with the color blue
        timer.tick(game_frames_per_second) 
        screen.fill(color_light_blue.three_nums) 

        #to write text of which nodes
        letter_text = pygame.font.Font('freesansbold.ttf',26).render("Finding The Shortest Path From "+str(source_node.letter)+" to "+str(destination_node.letter)+"", True, color_black.three_nums)
        screen.blit(letter_text, (100, screen_height-100)) #use these numbers to center it

        #draw the edges and nodes on the screem
        drawEdges()
        drawNodes()
        #print them on
        pygame.display.flip()

        #we can use the red x to kill the program in the window
        for event in pygame.event.get():
            #make our quit condition for the loop
            if event.type == pygame.QUIT:
                is_game_running = False

        #do breadth-first search
        if(not BFS_done):
            BFS_text = pygame.font.Font('freesansbold.ttf',26).render("Performing Breadth-First Search...", True, color_black.three_nums)
            screen.blit(BFS_text, (100, screen_height-50)) #use these numbers to center it

            time_bfs = time.time()
            #get our shortest path by running BFS
            BFS_shortestpath = BFS_shortest_path(vertices, edges, source_node, destination_node)
            time_bfs2 = time.time() -time_bfs - bfs_time_added 

            if(BFS_shortestpath != -10):
                BFS_letters = ""
                #get the text form of the shortest path so we can print it at the bottom
                for node in reversed(BFS_shortestpath):
                    BFS_letters+= str(node.letter)+"->"
                BFS_letters = BFS_letters[:-2] #get rid of the last arrow
                
                #Print the text on the bottom with the shortest path if they are connected
                pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
                BFS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Shortest Path is: "+BFS_letters, True, color_black.three_nums)
                screen.blit(BFS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
                pygame.display.flip()
                time.sleep(3)
            else:
                #here, it is the result text if the nodes are disconnected
                pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
                BFS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Source and Destination are Disconnected", True, color_black.three_nums)
                screen.blit(BFS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
                pygame.display.flip()
                time.sleep(3)

            BFS_done = True
        
        #do depth-first search
        if(not DFS_done):

            #make rectangle to cover the text on the bottom of BFS
            pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
            pygame.display.flip()
            #put the performing DFS text on
            DFS_text = pygame.font.Font('freesansbold.ttf',26).render("Performing Depth-First Search...", True, color_black.three_nums)
            screen.blit(DFS_text, (100, screen_height-50)) #use these numbers to center it

            #Graphic visual of DFS
            DFS(vertices, edges)

            #GET THE ACTUAL SHORTEST PATH WITH ALGORITHM BELOW 
            #use this to track the time
            time_dfs = time.time()
            all_DFS_paths(source_node, destination_node)
            #have to manipulate our list of chars so that we can get the smallest path
            fr_all_paths = list()
            indices_of_last = []
            #iterate through all the characters, since we couldn't add lists due to the recursive properties in the all_DFS_paths function
            for i in range(len(dfs_all_paths)):
                if(dfs_all_paths[i] == destination_node.letter): #count how many paths there are
                    indices_of_last.append(i)
                    #store all the indices of the destination nodes so we can split our arrays

            #now that we have indices of the end of the path, get each path through slicing
            for i in range(len(indices_of_last)):
                if(i==0):
                    fr_all_paths.append(dfs_all_paths[:indices_of_last[i]+1])
                else:
                    fr_all_paths.append(dfs_all_paths[indices_of_last[i-1]+1:indices_of_last[i]+1])
            
            #initialize our min path so that we can store it later. works if there is no path, as well
            min_path = []
            min_path_length = len(vertices)+1
            #find the shortest path to the destination vertex
            for lst in fr_all_paths:
                if len(lst) < min_path_length:
                    min_path = lst
                    min_path_length = len(min_path)
            #algorithm is done so we can get the final time
            time_dfs2 = time.time() - time_dfs

            #if there is a path between them, post this text
            if(len(min_path) != 0):
                DFS_letters = ""
                #get the text form of the shortest path so we can print it at the bottom
                for chr in (min_path):
                    DFS_letters+= str(chr)+"->"
                DFS_letters = DFS_letters[:-2] #get rid of the last arrow
                
                #Print the text on the bottom with the shortest path if they are connected
                pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
                DFS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Shortest Path is: "+DFS_letters, True, color_black.three_nums)
                screen.blit(DFS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
                pygame.display.flip()
                time.sleep(3)
            else:
                #there is no path and source and destination are disconnected
                pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
                DFS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Source and Destination are Disconnected", True, color_black.three_nums)
                screen.blit(DFS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
                pygame.display.flip()
                time.sleep(3)
                    

            DFS_done = True

        #do bi-directional search
        if(not BDS_done):
            #make rectangle to cover the text on the bottom of DFS
            pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
            #reset the nodes
            for v in vertices:
                v.color = color_white
                v.font_color = color_black
            drawNodes()

            pygame.display.flip()

            #put the text on the bottom to show bds is being done
            BDS_text = pygame.font.Font('freesansbold.ttf',26).render("Performing Bi-Directional Search...", True, color_black.three_nums)
            screen.blit(BDS_text, (100, screen_height-50)) #use these numbers to center it

            #Graphical representation of BDS (BFS x2)
            BFS(vertices, edges, source_node)
            time.sleep(1)
            
            #reset the nodes
            for v in vertices:
                v.color = color_white
                v.font_color = color_black
            drawNodes()

            #do BFS backwards as well
            BFS(vertices, edges, destination_node)

            #get the time for BDS
            time_bds = time.time()
            shortest_path = BiDirectional_Search(source_node, destination_node)
            #algorithm done, so we can get final time

            time_bds2 = time.time() - time_bds

            if(shortest_path != -1):
                BDS_letters = ""
                #get the text form of the shortest path so we can print it at the bottom
                for chr in (shortest_path):
                    BDS_letters+= str(chr)+"->"
                BDS_letters = BDS_letters[:-2] #get rid of the last arrow
                
                #Print the text on the bottom with the shortest path if they are connected
                pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
                BDS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Shortest Path is: "+BDS_letters, True, color_black.three_nums)
                screen.blit(BDS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
                pygame.display.flip()
                time.sleep(3)
            else:
                #there is no path and source and destination are disconnected
                pygame.draw.rect(screen,color_light_blue.three_nums, pygame.Rect(0,screen_height-50,screen_width,50))
                BDS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Source and Destination are Disconnected", True, color_black.three_nums)
                screen.blit(BDS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
                pygame.display.flip()
                time.sleep(3)

            BDS_done = True

        #write the 'done' text on the screen when we finish
        BFS_text_to_screen = pygame.font.Font('freesansbold.ttf',26).render("Done With All Algorithms.", True, color_black.three_nums)
        screen.blit(BFS_text_to_screen, (100, screen_height-50)) #use these numbers to center it
        pygame.display.flip()

    #Print the time each algorithm took after the graphical representation is closed
    #print("Time BFS: "+ str(time_bfs2)+"\nTime DFS: "+str(time_dfs2)+"\nTime BDS: "+str(time_bds2))
    pygame.quit()