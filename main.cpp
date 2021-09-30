#pragma GCC optimize("Ofast")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,avx2,fma")
#pragma GCC optimize("unroll-loops")
#include "bits/stdc++.h"
#include <complex>
#include <queue>
#include <set>
#include <unordered_set>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;
template <typename T>
using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;
#include <list>
#include <chrono>
#include <random>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <stack>
#include <iomanip>
#include <fstream>

typedef long long ll;
typedef long double ld;
typedef pair<int, int> p32;
typedef pair<ll, ll> p64;
typedef pair<double, double> pdd;
typedef vector<ll> v64;
typedef vector<int> v32;
typedef vector<vector<int>> vv32;
typedef vector<vector<ll>> vv64;
typedef vector<vector<p64>> vvp64;
typedef vector<p64> vp64;
typedef vector<p32> vp32;
ll MOD = 998244353;
double eps = 1e-12;
#define tr(container, it) for (typeof(container.begin()) it = container.begin(); it != container.end(); it++)
#define present(container, element) (container.find(element) != container.end())
#define cpresent(container, element) (find(all(container), element) != container.end())
#define all(c) c.begin(), c.end()
#define sz(c) c.size()
#define forn(i, e) for (ll i = 0; i < e; i++)
#define forsn(i, s, e) for (ll i = s; i < e; i++)
#define rforn(i, s) for (ll i = s; i >= 0; i--)
#define rforsn(i, s, e) for (ll i = s; i >= e; i--)
#define ln "\n"
#define dbg(x) cout << #x << " = " << x << ln
#define mp make_pair
#define pb push_back
#define fi first
#define se second
#define INF 2e9
#define fast_cin()                    \
    ios_base::sync_with_stdio(false); \
    cin.tie(NULL);                    \
    cout.tie(NULL)
// #define all(x) (x).begin(), (x).end()
// #define sz(x) ((ll)(x).size())

class Graph
{
public:
    vector<vector<pair<int, int>>> adj;
    int nodes;
    int edges;

    class Node
    {
    public:
        int current;
        Node *parent;
        Node(int c = -1, Node *p = NULL)
        {
            current = c;
            parent = p;
        }
        // Node(int c = -1)
        // {
        //     current = c;
        //     parent = NULL;
        // }
        bool operator<(const Node &d)
        {
            return current < d.current;
        }
    };
    struct Pq_element
    {
        int fvalue;
        int gvalue;
        int node;
        Node root;
        bool operator<(const Pq_element &rhs) const
        {
            if (fvalue == rhs.fvalue && gvalue == rhs.gvalue)
                return node > rhs.node;
            else if (fvalue == rhs.fvalue)
                return gvalue > rhs.gvalue;
            else
                return fvalue > rhs.fvalue;
        }
    };
    struct not_mst_set_element
    {
        int node;
        int source;
        int cost;
        // bool operator<(const not_mst_set_element &rhs) const
        // {
        //     if (fvalue == rhs.fvalue && gvalue == rhs.gvalue)
        //         return node > rhs.node;
        //     else if (fvalue == rhs.fvalue)
        //         return gvalue > rhs.gvalue;
        //     else
        //         return fvalue > rhs.fvalue;
        // }
    };
    Graph(int n, int e)
    {
        nodes = n;
        edges = e;
        adj = vector(n, vector<pair<int, int>>(0));
    }
    void printGraph()
    {
        forn(i, nodes)
        {
            cout << i << endl;
            for (auto it : adj[i])
                cout << it.first << " " << it.second << endl;
        }
    }
    vector<int> astar()
    {
        priority_queue<Pq_element> pq;
        Node root(-1, NULL);
        int expanded, generated = 0;
        pq.push(Pq_element{0, 0, 0, root});
        while (!pq.empty())
        {
            Pq_element element = pq.top();
            pq.pop();
            int gvalue = element.gvalue;
            int node = element.node;
            Node parent = element.root;
            // cout << gvalue << node << parent.current;
            Node cur = Node(node, &parent);
            vector<int> path = {node};
            Node *temp = cur.parent;
            while (temp->parent != NULL)
            {
                path.push_back(temp->current);
                temp = temp->parent;
            }
            if (path.size() == nodes + 1)
            {
                cout << "Cost for Travelling Salesman Problem: ";
                cout << "Number of nodes Expanded: " << expanded;
                cout << "Number of nodes Generated: " << generated;
                reverse(path.begin(), path.end());
                return path;
            }
            else
            {
                vector<int> al(nodes);
                iota(all(al), 0);
                vector<int> diff(nodes);
                std::vector<int>::iterator it, ls;
                ls = std::set_difference(all(al), all(path), diff.begin());
                vector<int> pat = get_MST(diff, ls);
                // for (it = diff.begin(); it < ls; ++it)
                //     std::cout << " " << *it;
                // std::cout << "\n";
                // cout << "hello";
                // forn(i, nodes)
                //         cout
                //     << al[i] << endl
                //     << endl;
                // for (auto it : path)
                //    cout << it << endl;

                return {};
            }
        }
    }

    vector<int> get_MST(vector<int> diff, vector<int>::iterator ls)
    {
        vector<pair<int, int>> mst;
        vector<not_mst_set_element> not_mst;
        if (ls == diff.begin())
        {
            forn(i, nodes)
                not_mst.push_back(not_mst_set_element{i, -1, INF});
        }
        else
        {
            for (vector<int>::iterator it = diff.begin(); it < ls; ++it)
                not_mst.push_back(not_mst_set_element{*it, -1, INF});
        }
        while (!not_mst.empty())
        {
            int min_node = find_min_key(not_mst);
            struct not_mst_set_element ret = not_mst[min_node];
            not_mst.erase(not_mst.begin() + min_node);
            mst.push_back({ret.node, min_node});
            for (auto it : idj[min_node])
            {
                for (auto itt : not_mst)
                {
                    if (it.first == itt.node)
                }
            }
        }
        return mst;
    }
};

int main()
{
    fast_cin();
    std::ifstream in("in.txt");
    std::streambuf *cinbuf = std::cin.rdbuf(); //save old buf
    std::cin.rdbuf(in.rdbuf());                //redirect std::cin to in.txt!

    std::ofstream out("out.txt");
    std::streambuf *coutbuf = std::cout.rdbuf(); //save old buf
    std::cout.rdbuf(out.rdbuf());                //redirect std::cout to out.txt!

    int nodes, edges;
    cin >> nodes >> edges;
    Graph graph(nodes, edges);
    forn(i, edges)
    {
        int a, b, wt;
        cin >> a >> b >> wt;
        graph.adj[a].push_back({b, wt});
        graph.adj[b].push_back({a, wt});
    }
    // graph.printGraph();
    graph.astar();
    // vector<int> path = graph.astar();
    // int sz = path_exp_gen_cost.size();
    // forn(i, sz - 3)
    //         cout
    //     << path_exp_gen_cost[i] << " ";
    // cout << "Cost for Travelling Salesman Problem: " << path_exp_gen_cost[sz - 1];
    // cout << "Number of nodes Expanded: " << path_exp_gen_cost[sz - 3];
    // cout << "Number of nodes Generated: " << path_exp_gen_cost[sz - 2];

    return 0;
}