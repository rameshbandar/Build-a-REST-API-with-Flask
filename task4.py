# Minimal Flask REST API without imports (using built-in Flask features)
class Flask:
    def _init_(self, name):
        self.name = name
        self.routes = {}

    def route(self, path, methods=["GET"]):
        def decorator(func):
            self.routes[(path, tuple(methods))] = func
            return func
        return decorator

    def run(self, debug=False):
        print(f" * Running {self.name} (simulated)")
        print(" * Endpoints:")
        for (path, methods), func in self.routes.items():
            print(f"   - {path} [{', '.join(methods)}]")

app = Flask(_name_)

# In-memory "database"
users = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
    2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
}

# Helper functions
def jsonify(data, status=200):
    return {"data": data, "status": status}

def get_next_id():
    return max(users.keys()) + 1 if users else 1

# Routes
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values()))

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(users.get(user_id, {"error": "Not found"}), 404 if user_id not in users else 200)

@app.route("/users", methods=["POST"])
def create_user():
    # Simulate request.json parsing
    new_id = get_next_id()
    users[new_id] = {"id": new_id, "name": "New User", "email": "new@example.com"}
    return jsonify(users[new_id], 201)

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id in users:
        users[user_id]["name"] = "Updated Name"
        return jsonify(users[user_id])
    return jsonify({"error": "Not found"}, 404)

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Not found"}, 404)

# Run the simulated app
app.run(debug=True)