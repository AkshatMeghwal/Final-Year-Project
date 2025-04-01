import os
import esprima
import networkx as nx
import openai

# OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Token limit for the AI model
TOKEN_LIMIT = 4000


def calculate_code_size(code):
    """Estimate the size of the code in tokens."""
    return len(code.split())


def parse_js_file(file_path):
    """Parse a JavaScript file to extract functions and their relationships."""
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    ast = esprima.parseScript(code, tolerant=True)
    functions = {}
    calls = []

    def traverse(node, parent_func=None):
        if node.type == 'FunctionDeclaration':
            func_name = node.id.name
            functions[func_name] = {
                "code": code[node.range[0]:node.range[1]],
                "calls": [],
                "file_path": file_path,
                "location": (node.loc.start.line, node.loc.end.line),
            }
            parent_func = func_name
        elif node.type == 'CallExpression' and parent_func:
            called_func = node.callee.name if hasattr(node.callee, 'name') else None
            if called_func:
                calls.append((parent_func, called_func))
                functions[parent_func]["calls"].append(called_func)

        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, esprima.nodes.Node):
                        traverse(item, parent_func)
            elif isinstance(value, esprima.nodes.Node):
                traverse(value, parent_func)

    traverse(ast)
    return functions, calls


def build_dependency_tree(functions, calls):
    """Build a dependency tree (directed graph) for functions."""
    graph = nx.DiGraph()
    for func in functions:
        graph.add_node(func, **functions[func])
    for parent, child in calls:
        if child in functions:
            graph.add_edge(parent, child)
    return graph


def traverse_for_tokens(graph):
    """Break functions into tokens, ensuring all children fit within the token limit."""
    tokens = []
    resolved = {}
    for func in nx.topological_sort(graph):
        children = list(graph.successors(func))
        child_contexts = [resolved[child] for child in children if child in resolved]

        # Combine code and child contexts
        func_code = graph.nodes[func]["code"]
        combined_context = "\n".join(child_contexts) + "\n" + func_code
        size = calculate_code_size(combined_context)

        if size <= TOKEN_LIMIT:
            resolved[func] = combined_context
            tokens.append((func, combined_context))
        else:
            raise ValueError(f"Function {func} exceeds the token limit with its children.")

    return tokens


def generate_context_in_batches(tokens):
    """Generate context for functions in batches."""
    contexts = {}
    for func, token in tokens:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Explain the following JavaScript function:\n\n{token}",
            max_tokens=1500,
            temperature=0.2,
        )
        contexts[func] = response.choices[0].text.strip()
    return contexts


def add_comments_to_code(file_path, contexts):
    """Embed comments into the original JavaScript code."""
    with open(file_path, 'r', encoding='utf-8') as f:
        code_lines = f.readlines()

    for func, context in contexts.items():
        loc = contexts[func]["location"]
        comment = f"/**\n * {context.replace('\n', '\n * ')}\n */\n"
        code_lines.insert(loc[0] - 1, comment)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(code_lines)


def process_project(directory):
    """Process a project by breaking it into tokens and embedding comments."""
    all_functions = {}
    all_calls = []

    # Parse all JavaScript files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                functions, calls = parse_js_file(file_path)
                all_functions.update(functions)
                all_calls.extend(calls)

    # Build dependency tree
    graph = build_dependency_tree(all_functions, all_calls)

    # Break into tokens
    tokens = traverse_for_tokens(graph)

    # Generate contexts
    contexts = generate_context_in_batches(tokens)

    # Add comments to code
    for func, details in all_functions.items():
        add_comments_to_code(details["file_path"], {func: contexts[func]})


# Process a sample project directory
process_project("path_to_your_project")
