from collections import deque


class FVertex:
    """
    A class that represents a vertex in a flow network.

    Each vertex maintains a list of outgoing edges and has a unique identifier.
    This is used to build the adjacency list representation of the flow network.
    """

    def __init__(self, id):
        """
        Function description: Initializes a vertex with given ID.

        Input:
            id: The ID for this vertex

        Time complexity: O(1), constant time initialization
        Time complexity analysis: The constructor only assigns the ID and creates an empty list, both constant time operations.

        Space complexity: O(1), stores only ID and empty edge list
        Space complexity analysis: The constructor stores only the vertex ID and initializes an empty edge list, both requiring constant space.
        """
        self.id = id
        self.edges = []

    def add_edge(self, edge):
        """
        Function description: Adds an outgoing edge to this vertex.

        Input:
            edge: FEdge object representing the outgoing edge

        Time complexity: O(1), constant time list append
        Time complexity analysis: The function performs a single list append operation which is constant time.

        Space complexity: O(1), only stores reference to edge
        Space complexity analysis: The function only stores a reference to the edge object, requiring constant additional space.
        """
        self.edges.append(edge)


class FEdge:
    """
    A class that represents an edge in a flow network.

    Each edge stores the source vertex, destination vertex, current flow,
    maximum capacity, and residual capacity for efficient flow computations.
    """

    def __init__(self, u, v, flow, max_capacity):
        """
        Function description: Initializes a flow edge with specified parameters.

        Input:
            u: Source vertex (FVertex)
            v: Destination vertex (FVertex)
            flow: Current flow through the edge
            max_capacity: Maximum capacity of the edge

        Time complexity: O(1), constant time initialization
        Time complexity analysis: The constructor only assigns attributes and performs one subtraction, all constant time operations.

        Space complexity: O(1), stores only the edge attributes
        Space complexity analysis: The constructor stores the edge parameters and computed residual value, requiring constant space.
        """
        self.u = u
        self.v = v  # Adjacent/neighbor vertex
        self.flow = flow
        self.max_capacity = max_capacity
        self.residual = max_capacity - flow


class FlowNetwork:
    """
    A class that represents a flow network using an adjacency list representation.

    This class maintains the flow network structure with vertices and edges,
    supporting directed graphs for maximum flow computations.
    """

    def __init__(self, argv_vertices_count):
        """
        Function description: Initializes a flow network with specified number of vertices.

        Input:
            argv_vertices_count: The number of vertices in the graph

        Time complexity: O(V), where V is the number of vertices
        Time complexity analysis: Creates V vertex objects in a list comprehension.

        Space complexity: O(V), for storing vertex objects
        Space complexity analysis: Stores a list containing V vertex objects.
        """
        # Adjacency list representation
        self.vertices = [FVertex(i) for i in range(argv_vertices_count)]

    def add_edges(self, argv_edges, argv_directed=True):
        """
        Function description: Adds edges to the flow network.

        Input:
            argv_edges: List of tuples (u, v, flow, capacity) representing edges
            argv_directed: Boolean indicating if graph is directed (default True)

        Time complexity: O(E), where E is the number of edges to add
        Time complexity analysis: Iterates through each edge once, performing constant time operations for each edge.

        Space complexity: O(E), for storing edge objects
        Space complexity analysis: Creates one FEdge object for each edge (or two for undirected graphs).
        """
        for edge in argv_edges:
            u: FVertex = self.vertices[edge[0]]
            v: FVertex = self.vertices[edge[1]]
            flow = edge[2]
            capacity = edge[3]
            # add u to v
            current_edge = FEdge(u, v, flow, capacity)
            current_vertex = u
            current_vertex.add_edge(current_edge)
            if not argv_directed:
                # add v to u
                current_edge = FEdge(v, u, flow, capacity)
                current_vertex = v
                current_vertex.add_edge(current_edge)


class RVertex:
    """
    A class that represents a vertex in a residual network.

    Extends basic vertex functionality with BFS traversal attributes
    for efficient path finding in the residual graph.
    """

    def __init__(self, id):
        """
        Function description: Initializes a residual network vertex.

        Input:
            id: The ID for this vertex

        Time complexity: O(1), constant time initialization
        Time complexity analysis: The constructor assigns ID and initializes attributes, all constant time operations.

        Space complexity: O(1), stores vertex attributes
        Space complexity analysis: The constructor stores the vertex ID and BFS state variables, requiring constant space.
        """
        self.id = id
        self.edges = []
        self.discovered = False  # BFS discovery state
        self.visited = False  # BFS visit state
        self.prev = None  # Previous edge in BFS path

    def add_edge(self, edge):
        """
        Function description: Adds an edge to this residual vertex.

        Input:
            edge: ForwardEdge or BackwardEdge object

        Time complexity: O(1), constant time list append
        Time complexity analysis: The function performs a single list append operation which is constant time.

        Space complexity: O(1), only stores reference to edge
        Space complexity analysis: The function only stores a reference to the edge object, requiring constant additional space.
        """
        self.edges.append(edge)


class ForwardEdge:
    """
    A class representing a forward edge in the residual network.

    Forward edges represent the remaining capacity on an original edge,
    allowing additional flow to be pushed in the forward direction.
    Each forward edge maintains a mirror reference to its corresponding    backward edge for efficient augmentation operations.
    """

    def __init__(self, u, v, w, original_edge):
        """
        Function description: Initializes a forward edge in the residual network.

        Input:
            u: Source vertex of the edge
            v: Destination vertex of the edge
            w: Residual capacity (remaining capacity for forward flow)
            original_edge: Reference to the original flow edge for updating flow values

        Time complexity: O(1), constant time initialization
        Time complexity analysis: The constructor only assigns attributes, all constant time operations.

        Space complexity: O(1), stores edge attributes and references
        Space complexity analysis: The constructor stores the edge parameters and references, requiring constant space.
        """
        self.u = u
        self.v = v
        self.w = w
        self.original_edge = (
            original_edge  # reference to original flow edge for updating
        )
        self.mirror = None  # reference to corresponding backward edge for O(1) access


class BackwardEdge:
    """
    A class representing a backward edge in the residual network.

    Backward edges represent the current flow on an original edge,
    allowing flow to be "undone" by pushing flow in the reverse direction.
    Each backward edge maintains a mirror reference to its corresponding    forward edge for efficient augmentation operations.
    """

    def __init__(self, u, v, w, original_edge):
        """
        Function description: Initializes a backward edge in the residual network.

        Input:
            u: Source vertex of the edge (reverse direction of original)
            v: Destination vertex of the edge (reverse direction of original)
            w: Current flow capacity (amount of flow that can be undone)
            original_edge: Reference to the original flow edge for updating flow values

        Time complexity: O(1), constant time initialization
        Time complexity analysis: The constructor only assigns attributes, all constant time operations.

        Space complexity: O(1), stores edge attributes and references
        Space complexity analysis: The constructor stores the edge parameters and references, requiring constant space.
        """
        self.u = u
        self.v = v
        self.w = w
        self.original_edge = (
            original_edge  # reference to original flow edge for updating
        )
        self.mirror = None  # reference to corresponding forward edge for O(1) access


class ResidualNetwork:
    """
    A class that represents a residual network using an adjacency list representation.

    The residual network is constructed from a flow network and contains forward edges
    (representing remaining capacity) and backward edges (representing current flow
    that can be undone). This representation enables efficient Ford-Fulkerson algorithm
    implementation with mirror edge optimization for O(1) edge updates.
    """

    def __init__(self, flow_network):
        """
        Function description: Initializes a residual network from a flow network.

        Creates vertices and builds the complete residual network with forward
        and backward edges, establishing mirror relationships for efficiency.

        Input:
            flow_network: The flow network to create the residual network from

        Time complexity: O(V + E), where V is vertices and E is edges
        Time complexity analysis: Creates V vertices in O(V) time, then calls build_residual_network which processes all E edges in O(V + E) time.

        Space complexity: O(V + E), for storing residual network structure
        Space complexity analysis: Stores V residual vertices and up to 2E residual edges (forward and backward).
        """
        self.flow_network = flow_network
        self.vertices = [
            RVertex(i) for i in range(len(flow_network.vertices))
        ]  # adjacency list representation
        self.build_residual_network()

    def build_residual_network(self):
        """
        Function description: Constructs the residual network from the flow network.

        Creates forward and backward edges with mirror relationships for each
        original edge. Forward edges have capacity = residual capacity,
        backward edges have capacity = current flow.

        Time complexity: O(V + E), where V is vertices and E is edges
        Time complexity analysis: Clears edges for V vertices in O(V) time, then processes each of E edges to create forward and backward edges in O(E) time.

        Space complexity: O(E), for creating residual edges
        Space complexity analysis: Creates up to 2E residual edges (forward and backward) for E original edges.
        """
        # Reset all edges in the residual network before rebuilding
        for vertex in self.vertices:
            vertex.edges = []  # Clear all existing edges

        # Build residual network from flow network
        for f_u in self.flow_network.vertices:
            for f_edge in f_u.edges:
                r_u: RVertex = self.vertices[f_u.id]
                r_v: RVertex = self.vertices[f_edge.v.id]
                residual = f_edge.residual
                flow = f_edge.flow
                f_edge: FEdge = f_edge

                # Create forward and backward edges
                forward_edge = ForwardEdge(r_u, r_v, residual, f_edge)
                backward_edge = BackwardEdge(r_v, r_u, flow, f_edge)

                # Establish mirror relationship for O(1) access
                forward_edge.mirror = backward_edge
                backward_edge.mirror = forward_edge

                # Always add edges (even with zero capacity) to avoid expensive deletions
                # BFS will skip zero-capacity edges during traversal
                self.vertices[r_u.id].add_edge(forward_edge)
                self.vertices[r_v.id].add_edge(backward_edge)

    def reset(self):
        """
        Function description: Resets BFS state for all vertices in the residual network.

        Clears discovered, visited, and previous edge information for a fresh BFS traversal.

        Time complexity: O(V), where V is the number of vertices
        Time complexity analysis: Iterates through all V vertices to reset their BFS state attributes.

        Space complexity: O(1), only modifies existing vertex attributes
        Space complexity analysis: Only modifies existing vertex attributes without allocating new memory.
        """
        for vertex in self.vertices:
            vertex.discovered = False
            vertex.visited = False
            vertex.prev = None

    def get_augmenting_path(self, source, target):
        """
        Function description: Finds an augmenting path from source to target vertex in the residual network using breadth-first search traversal.

        Input:
            source: An integer representing the source vertex ID for path finding
            target: An integer representing the target vertex ID for path finding

        Output: A list of edges forming the augmenting path from source to target (empty list if no path exists)

        Time complexity: O(V + E), where V is the number of vertices and E is the number of edges
        Time complexity analysis: BFS visits each vertex at most once in O(V) time and examines each edge at most once in O(E) time, giving O(V + E) total complexity.

        Space complexity: O(V), for the BFS queue and vertex state tracking
        Space complexity analysis: The BFS queue can contain at most V vertices, and vertex state variables require O(V) space.
        """
        self.reset()
        source_vertex: RVertex = self.vertices[source]
        target_vertex: RVertex = self.vertices[target]
        discovered = deque()
        discovered.append(source_vertex)
        source_vertex.discovered = True

        # BFS to find augmenting path
        while len(discovered) > 0:
            # Serve from queue
            u: RVertex = discovered.popleft()
            u.visited = True

            for edge in u.edges:
                v: RVertex = edge.v
                # Check if the edge has capacity and vertex is unvisited
                if v.discovered == False and v.visited == False and edge.w > 0:
                    discovered.append(v)  # add the vertex to our queue
                    v.discovered = True  # mark the vertex as discovered
                    v.prev = edge  # Store the edge instead of vertex for efficiency

        # Check if target is reachable
        if target_vertex.discovered == False:
            return []  # No path exists

        # backtrack to find the augmenting path (returning edges)
        augmenting_path = []
        current_vertex = target_vertex
        while current_vertex.prev is not None:
            edge = current_vertex.prev
            augmenting_path.append(edge)
            current_vertex = edge.u
        augmenting_path.reverse()

        return augmenting_path

    def get_residual_capacity(self, path):
        """
        Function description: Calculates the residual capacity of the augmenting path.
        This is the bottleneck capacity - minimum capacity along the path.

        Input:
            path: A list of edges forming the augmenting path

        Output: An integer representing the minimum capacity along the path (bottleneck)

        Time complexity: O(P), where P is the length of the path
        Time complexity analysis: Iterates through each edge in the path once to find the minimum capacity.

        Space complexity: O(1), using only constant additional space
        Space complexity analysis: Uses only a single variable to track the bottleneck value.
        """
        bottleneck = float("inf")
        for edge in path:
            bottleneck = min(bottleneck, edge.w)
        return bottleneck

    def augment_flow(self, path):
        """
        Function description: Augments the flow along the augmenting path and updates
        only the affected edges in the residual network for efficiency.

        Input:
            path: A list of edges forming the augmenting path

        Time complexity: O(P), where P is the length of the path
        Time complexity analysis: Iterates through each edge in the path once to update capacities and flows.

        Space complexity: O(1), using only constant additional space
        Space complexity analysis: Uses only a bottleneck variable and modifies existing edge capacities in-place.
        """
        # Get the residual capacity of the path (bottleneck)
        bottleneck = self.get_residual_capacity(path)

        # Update flow along the path using mirror edges for O(1) efficiency
        for e in path:
            # Update this edge capacity
            e.w -= bottleneck
            # Update mirror edge capacity using O(1) access
            e.mirror.w += bottleneck

            # Update original flow based on edge type
            if isinstance(e, ForwardEdge):
                # Forward edge: increase flow
                e.original_edge.flow += bottleneck
                e.original_edge.residual -= bottleneck
            else:
                # Backward edge: decrease flow (undo operation)
                # Handle backward edge
                e: BackwardEdge = e
                e.original_edge.flow -= bottleneck
                e.original_edge.residual += bottleneck


def ford_fulkerson(my_graph):
    """
    Function description: Implements the Ford-Fulkerson algorithm to compute the maximum flow in a flow network using BFS for finding augmenting paths.

    Input:
        my_graph: A FlowNetwork object representing the flow network

    Output: An integer representing the maximum flow value from source to sink

    Time complexity: O(V * E^2), where V is the number of vertices and E is the number of edges

    Time complexity analysis: Ford-Fulkerson runs in O(F * E) where F is the maximum flow value. Each of the F iterations requires finding an augmenting path using BFS. When E >= V-1 (connected graph), BFS complexity becomes O(E) since E dominates. In worst case F <= V*E (bounded by cut capacity), giving O(V*E*E) = O(V*E^2). The E^2 factor comes from potentially augmenting and later reversing flow on edges.

    Space complexity: O(V + E), for the residual network and BFS data structures
    Space complexity analysis: The residual network requires O(V + E) space for vertices and edges. BFS uses O(V) additional space for the queue and vertex state tracking.
    """
    # initialize flow
    flow = 0
    # initialize the residual network
    residual_network = ResidualNetwork(my_graph)
    # extract the source and target vertices
    source = 0
    target = len(residual_network.vertices) - 1
    for edge in my_graph.vertices[source].edges:
        edge: FEdge = edge
        flow += edge.flow

    # as long as there is a augmenting path, take the path
    path = residual_network.get_augmenting_path(source, target)
    while len(path) > 0:
        # augment the flow equal to the residual capacity (bottleneck)
        flow += residual_network.get_residual_capacity(path)
        # updating the residual network along the path
        residual_network.augment_flow(path)
        # get next path
        path = residual_network.get_augmenting_path(source, target)
    return flow


def allocate_students(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
    Function description: Allocates n students to m proposed classes so that every student gets exactly one
    class, every class size stays within [min_students, max_students], and at least minimumSatisfaction
    students are placed in a class whose time slot is one of their top-5 preferences.

    Approach description:
    The problem is modelled as a flow network with lower bounds and solved as a feasible circulation.
    1. source -> student i                  [1, 1]   every student must be allocated
    2. student i -> class j                 [0, 1]   only if class j's time slot is in student i's top 5
    3. student i -> unsatisfied_in          [0, 1]   the "not in top 5" route
    4. unsatisfied_in -> unsatisfied_out    [0, n - minimumSatisfaction]   caps how many students miss their top 5
    5. unsatisfied_out -> class j           [0, n]   every student can attend every slot, so any class is allowed
    6. class j -> sink                      [min_j, max_j]   class size limits
    7. sink -> source                       [0, n]   turns the network into a circulation
    Lower bounds are removed with the standard transformation: each edge (u, v, l, c) becomes (u, v, c - l), and
    the l units become demands met through a super-source and a super-sink. A feasible allocation exists exactly
    when Ford-Fulkerson saturates every super-source edge. Students routed through the unsatisfied node are
    interchangeable (every student accepts every slot), so they are paired with the class units that node sends
    out in any order.

    Input:
        n: A positive integer representing the number of students to be allocated
        m: A positive integer representing the number of proposed classes
        timePreferences: A list of lists where timePreferences[i] is a permutation of time slots 0-19 in order of preference for student i
        proposedClasses: A list of lists where proposedClasses[j] = [timeslot, min_students, max_students] for class j
        minimumSatisfaction: A non-negative integer, the minimum number of students who must get a top-5 time slot

    Output:
        A list where allocation[i] is the class assigned to student i, or None if no valid allocation exists

    Time complexity: O(n^2 * m)
    Time complexity analysis: The network has O(n + m) vertices and O(n * m) edges (each student links to at most
        the classes in its top-5 slots, plus one unsatisfied edge). Ford-Fulkerson with BFS finds each augmenting path
        in O(n * m) and the total flow is at most 2n (n units from the student lower bounds plus at most n from the
        class lower bounds), giving O(n * m * n) = O(n^2 * m). Building the allocation is O(n * m).

    Space complexity: O(n * m)
    Space complexity analysis: The flow network and its residual network each store O(n * m) edges.
    """
    if minimumSatisfaction > n:
        return None

    class_timeslots = [proposedClasses[j][0] for j in range(m)]
    min_students = [proposedClasses[j][1] for j in range(m)]
    max_students = [proposedClasses[j][2] for j in range(m)]
    if sum(min_students) > n or sum(max_students) < n or any(lo > hi for lo, hi in zip(min_students, max_students)):
        return None

    # vertex ids: the super-source must be 0 and the super-sink the last vertex (ford_fulkerson's convention)
    super_source = 0
    student_vertex = lambda i: 1 + i
    class_vertex = lambda j: 1 + n + j
    unsatisfied_in = 1 + n + m
    unsatisfied_out = unsatisfied_in + 1
    source = unsatisfied_out + 1
    sink = source + 1
    super_sink = sink + 1
    total_vertices = super_sink + 1

    # edges with lower bounds: (u, v, lower, capacity)
    bounded_edges = []
    for i in range(n):
        bounded_edges.append((source, student_vertex(i), 1, 1))
        top_slots = set(timePreferences[i][:5])
        for j in range(m):
            if class_timeslots[j] in top_slots:
                bounded_edges.append((student_vertex(i), class_vertex(j), 0, 1))
        bounded_edges.append((student_vertex(i), unsatisfied_in, 0, 1))
    bounded_edges.append((unsatisfied_in, unsatisfied_out, 0, n - minimumSatisfaction))
    for j in range(m):
        bounded_edges.append((unsatisfied_out, class_vertex(j), 0, n))
        bounded_edges.append((class_vertex(j), sink, min_students[j], max_students[j]))
    bounded_edges.append((sink, source, 0, n))

    # remove lower bounds: keep (capacity - lower) and turn the lower bounds into vertex demands
    excess = [0] * total_vertices
    edges = []
    edge_index = {}
    for u, v, lower, capacity in bounded_edges:
        edge_index[(u, v)] = len(edges)
        edges.append((u, v, 0, capacity - lower))
        excess[v] += lower
        excess[u] -= lower
    required = 0
    for vertex in range(total_vertices):
        if excess[vertex] > 0:
            edges.append((super_source, vertex, 0, excess[vertex]))
            required += excess[vertex]
        elif excess[vertex] < 0:
            edges.append((vertex, super_sink, 0, -excess[vertex]))

    flow_network = FlowNetwork(total_vertices)
    flow_network.add_edges(edges)
    if ford_fulkerson(flow_network) != required:
        return None

    # read the allocation back from the flow
    allocation = [None] * n
    unsatisfied_students = []
    for i in range(n):
        for edge in flow_network.vertices[student_vertex(i)].edges:
            if edge.flow > 0:
                if edge.v.id == unsatisfied_in:
                    unsatisfied_students.append(i)
                elif n < edge.v.id <= n + m:
                    allocation[i] = edge.v.id - n - 1
                break
    unsatisfied_slots = []
    for edge in flow_network.vertices[unsatisfied_out].edges:
        unsatisfied_slots.extend([edge.v.id - n - 1] * edge.flow)
    for i, j in zip(unsatisfied_students, unsatisfied_slots):
        allocation[i] = j

    return allocation
