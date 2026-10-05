#include <bits/stdc++.h>
using namespace std;

int main(int argc, char* argv[]) {
    unordered_map<long long, vector<pair<long long, double>>> graph;
    
    ifstream file("graph_data.txt");
    long long u, v;
    double w;
    
    while (file >> u >> v >> w) {
        graph[u].push_back({v, w});

        graph[v].push_back({u,w});
        // If bidirectional, also add:
        // graph[v].push_back({u, w});
    }
    
    file.close();
    cout << "Graph loaded successfully!" << endl;

    
    
    long long Start_node;
    long long End_node;
    long long Blocked_node1;
    long long Blocked_node2;


    if (argc != 5) {
        cerr << "Usage: dijkstra.exe START_NODE END_NODE" << endl;
        return 1;
    }


    if(argc == 5){
        Start_node = stoll(argv[1]);
        End_node = stoll(argv[2]);
        Blocked_node1 = stoll(argv[3]);
        Blocked_node2 = stoll(argv[4]);
    }
    // else if(argc == 3){
    //     Start_node = stoll(argv[1]);
    //     End_node = stoll(argv[2]);
    //     Blocked_node =  -1;
    // }




    cout<<graph[Start_node][0].first;
    long long total_node = graph.size();

    unordered_map<long long,double>vis;

    priority_queue<pair<double,long long>,vector<pair<double,long long>>,greater<pair<double,long long>>>pq;

    pq.push({0,Start_node});

    unordered_map<long long,long long>sequence;
    sequence[Start_node] = -1;

    int i = 0;
    bool found = false;
    while(!pq.empty()){
        cout<<++i<<endl;
        double dist = pq.top().first;
        long long node = pq.top().second;
        pq.pop();


        if(node == End_node){
            cout<<dist<<endl;
            found = true;
            break;
        }
        //cout<<i<<endl;
        for(auto it : graph[node]){
            long long nbr = it.first;
            double weigth = it.second;

            if(nbr == Blocked_node1 || nbr == Blocked_node2){
                continue;
            }

            if(!vis[nbr]){
                vis[nbr] = dist + weigth;
                sequence[nbr] = node;
                pq.push({vis[nbr],nbr});
                //cout<<++i<<endl;
            }
            else if (vis[nbr] > dist + weigth){
                //cout<<"repeated"<<endl;
                vis[nbr] = dist + weigth;
                sequence[nbr] = node;
                pq.push({vis[nbr],nbr});
            }
        }

    }

    if(!found){
        cout << "No path exists between the two nodes." << endl;

        ofstream pathFile("path.txt");

        if (!pathFile) {
            cerr << "Error: Could not create path.txt" << endl;
            return 1;
        }

        pathFile << "NO_PATH" << endl;

        pathFile.close();

        return 0;
    }


       
        cout<<"total_distance = "<<vis[End_node]<<"m"<<endl;
        vector<long long>path;
        long long node = End_node;
        path.push_back(End_node);
        cout<<End_node<<" ";
        while(node != Start_node){
            
            cout<<sequence[node]<<" ";
            path.push_back(sequence[node]);
            node = sequence[node];
        }

        cout<<endl;

        reverse(path.begin(),path.end());




        ofstream pathFile("path.txt");

        if (!pathFile) {

            cerr << "Error: Could not create path.txt"
                << endl;

            return 1;
        }


        
        pathFile << "START " << Start_node << endl;

        
        pathFile << "END " << End_node << endl;

        
        pathFile << "DISTANCE " << vis[End_node]<<"m"<< endl;

        
        pathFile << "NODES " << path.size() << endl;


        pathFile << "PATH" << endl;

        for (long long n : path) {

            pathFile << n << endl;
        }


        pathFile.close();


        cout << "\nPath successfully written to path.txt"
            << endl;

        return 0;
    
    

    
    return 0;
}