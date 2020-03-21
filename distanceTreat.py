import sys
import os.path
import numpy as np
import requests 
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw



def loadFile(fname):
    #print("fname: " + fname)
    if os.path.isfile(fname):
        file = open(fname, "r")
        content = file.read()
        #print(content)
        return content
    else:
        return "File not exist"



def parseLines(txt):
    object_type=""; track_id=""; minTime=""; maxTime=""; order_no="";
    Lines = []
    words = txt.split("\n")
    for word in words:
      if(word != ""): 
        #print(word)
        insider = [];
        items = word.split(";")
        if (items !=""):
            i = 0;
            for item in items:
                if (i == 0): object_type = item;
                if (i == 1 or i == 2):
                    insider.append(item);
                if (i == 3): track_id = item;
                if (i == 4): 
                    if (minTime == ""): minTime = item;
                    maxTime = item;
                if (i == 5): order_no = item;
                i +=1;
            Lines.append(insider);

    return object_type, track_id, minTime, maxTime, order_no, Lines;



if __name__ == '__main__':
    Benchmark_INBOUND_middle = np.array([[214,1], [217,4], [223,102], [228,116], [234,126], [228,133], [245,136], [254,139], [262,144], [258,164], [257,167], [255,171], [253,180], [251,180], [243,181], [251,182], [243,182], [227,183], [217,184], [200,185], [179,187], [166,189], [158,190], [152,195], [150,200], [143,200]]);
    Benchmark_INBOUND_right = np.array([[354,0], [363,0], [365,0], [368,0], [382,11], [385,12], [388,12], [397,46], [403,62], [406,63], [409,64], [407,85], [410,96], [411,105], [419,109], [426,112], [430,114], [421,123], [424,125], [426,127], [429,129], [431,130], [433,132], [436,134], [438,135], [441,137], [443,139], [446,141], [448,142], [450,144], [453,146], [455,147], [458,149], [460,151], [462,153], [465,154], [467,156], [470,158], [472,160], [474,161], [477,163]]);
    Benchmark_HOVER_middle = np.array([[220,0], [230,1], [240,4], [260,30], [250,50], [255,73], [245,90], [250,75], [245,64], [250,35], [255,20], [260,8], [240,4], [245,0], [250,0]]);
    Benchmark_HOVER_right = np.array([[395,0], [406,0], [412,1], [415,1], [418,1], [419,0], [421,0], [419,0], [419,2], [418,1], [417,2], [416,1], [416,1], [416,0], [415,0], [415,0], [412,3], [413,2], [413,5], [408,5], [408,6], [408,6], [408,6], [408,6], [408,6], [408,6], [408,6], [408,6], [408,6], [408,6], [408,7], [408,7], [408,7], [408,7], [408,7], [408,7], [408,7], [408,7], [408,7], [408,7]]);

    json = "{\"objects\":[";
    for f in range(1,15):
        fname = "track" + str(f) + ".csv";
        print(fname)
        if os.path.exists(fname):
            #if os.path.isfile(fname):
            file = open(fname, "r")
            content = file.read()
            print(fname + "" + str(len(content)))


            minDist = 0; minCaption=""; caption=""; order_no="";
            #content = loadFile(first_arg);

            xLines = [];
            object_type, track_id, minTime, maxTime, order_no, xLines = parseLines(content);
            #print("object_id: " + object_id + ", track_id: " + track_id + ", minTime: " + minTime + ", maxTime: " + maxTime);

            x = np.array( xLines ); y = x;

            print("N.B. INBOUND means that product was put into the cart, HOVER - product did not go into cart");
            for i in range(1,5):
                if (i==1): y = Benchmark_INBOUND_middle; caption = "INBOUND_middle";
                if (i==2): y = Benchmark_INBOUND_right; caption = "INBOUND_right";
                if (i==3): y = Benchmark_HOVER_middle; caption = "HOVER_middle";
                if (i==4): y = Benchmark_HOVER_right; caption = "HOVER_right";

                distance, path = fastdtw(x, y, dist=euclidean);
                #print("i: " + str(i) + ", distance: " + str(distance))
                if (i==1): minDist = distance;
                if (minDist >= distance): minDist = distance; minCaption = caption;
                #print("minDist: " + str(minDist) + ", minCaption: " + minCaption)
            print("distance: " + str(distance));
            print("Found: " + str(f) + ". '" + minCaption + "': closest distance: " + str(minDist));
            if (len(json) >10): json +=", ";
            json +="{\"object_type\":" + object_type + ", \"track_id\":" + track_id + ", \"minTime\":" + minTime + ", \"maxTime\":" + maxTime + ", \"distance\":" + str(minDist) + ", \"caption\":\"" + minCaption + "\", \"order_no\":\"" + order_no + "\"}";

    json +="]}";
    if os.path.exists("json_output.json"):
        os.remove("json_output.json");
    fw = open("json_output.json", "x");

    #json="{\"object_type\":" + object_type + ", \"track_id\":" + track_id + ", \"minTime\":" + minTime + ", \"maxTime\":" + maxTime + ", \"distance\":" + str(minDist) + ", \"caption\":\"" + minCaption + "\" }";
    print(json + "\n\n")
    fw.write(json);
    fw.close();


    URL = "https://app.virca.net/api/YoloDistance"
    try:
        r = requests.post(URL, data = json, headers = {"Content-Type": "application/json"})
        data = r.json() 
        print("Server response: " + str(data))
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)     


