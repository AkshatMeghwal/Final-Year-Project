import multiprocessing
import time
import api_calls

# Initialize the shared object globally
ai = api_calls.gemini_ai()

# Function for the first process
def process_one():
    for i in range(5):

        # if(comm!=i):
        #     print("Process one broken")
        #     break
        # comm+=1
        out=ai.get_outputcoderaw_geminiai(f"add two numbers ",f" 9 and {i}"," Ok i will add")
        print(f"{out}\n")
        # time.sleep(1)

# Function for the second process
def process_two():
    for i in range(5):
        out = ai.get_outputcoderaw_geminiai(f"add two numbers ",f" 5 and {i}"," Ok i will add")
        print(f"{out}\n")
        # time.sleep(1.5)

if __name__ == "__main__":
    # Create two Process objects
    p1 = multiprocessing.Process(target=process_one)
    p2 = multiprocessing.Process(target=process_two)

    # Start both processes
    p2.start()
    p1.start()

    # Wait for both processes to finish
    p2.join()







# import tree_sitter_javascript as tsjavascript
# from tree_sitter import Language, Parser

# JS_LANGUAGE = Language(tsjavascript.language())
# src=""
# def read_callable_byte_offset(byte_offset, point):
#     return src[byte_offset : byte_offset + 1]
# parser = Parser(JS_LANGUAGE)
# # with open("E:\Testing_folder\auth and api\API_Handling.js", "rb") as f:
# #     src = f.read()
# # src = bytes(
# #     """let x = 1;
# #     console.log(x);""",
# #     "utf8",
# # )
# # tree = parser.parse(
# #     src
# # )

# # tree = parser.parse(read_callable_byte_offset, encoding="utf8")

# # walked = tree.walk()
# # root_node = tree.root_node
# # print(tree.print_dot_graph)

# def remove_comments_from_js(js_code):
#     """
#     Removes comments from the given JavaScript code using Tree-sitter.
#     """
#     parser = Parser(JS_LANGUAGE)
#     tree = parser.parse(bytes(js_code, "utf8"))
#     root_node = tree.root_node

#     def traverse_and_collect(node):
#         """
#         Recursively traverse the syntax tree and collect non-comment code.
#         """
#         if node.type in ["comment", "ERROR"]:
#             return ""
#         if len(node.children) == 0:
#             return js_code[node.start_byte:node.end_byte]
#         return "".join(traverse_and_collect(child) for child in node.children)

#     return traverse_and_collect(root_node)

# # Example usage
# js_code = """
# // This is a single-line comment
# let x = 1; /* This is a multi-line comment */
# let y= 7;
# console.log(x); // Another comment
# """
# cleaned_code = remove_comments_from_js(js_code)
# print("Code without comments:")
# print(cleaned_code)























# import tree_sitter_javascript as tsjavascript
# from tree_sitter import Language, Parser

# JS_LANGUAGE = Language(tsjavascript.language())
# src=""
# def read_callable_byte_offset(byte_offset, point):
#     return src[byte_offset : byte_offset + 1]
# parser = Parser(JS_LANGUAGE)
# # with open("E:\Testing_folder\auth and api\API_Handling.js", "rb") as f:
# #     src = f.read()
# # src = bytes(
# #     """let x = 1;
# #     console.log(x);""",
# #     "utf8",
# # )
# # tree = parser.parse(
# #     src
# # )

# # tree = parser.parse(read_callable_byte_offset, encoding="utf8")

# # walked = tree.walk()
# # root_node = tree.root_node
# # print(tree.print_dot_graph)

# def remove_comments_from_js(js_code):
#     """
#     Removes comments from the given JavaScript code using Tree-sitter.
#     """
#     parser = Parser(JS_LANGUAGE)
#     tree = parser.parse(bytes(js_code, "utf8"))
#     root_node = tree.root_node

#     def traverse_and_collect(node):
#         """
#         Recursively traverse the syntax tree and collect non-comment code.
#         """
#         if node.type in ["comment", "ERROR"]:
#             return ""
#         if len(node.children) == 0:
#             return js_code[node.start_byte:node.end_byte]
#         return "".join(traverse_and_collect(child) for child in node.children)

#     return traverse_and_collect(root_node)

# # Example usage
# js_code = """
# // This is a single-line comment
# let x = 1; /* This is a multi-line comment */
# let y= 7;
# console.log(x); // Another comment
# """
# cleaned_code = remove_comments_from_js(js_code)
# print("Code without comments:")
# print(cleaned_code)

























# import tree_sitter_javascript as tsjavascript
# from tree_sitter import Language, Parser

# JS_LANGUAGE = Language(tsjavascript.language())
# src=""
# def read_callable_byte_offset(byte_offset, point):
#     return src[byte_offset : byte_offset + 1]
# parser = Parser(JS_LANGUAGE)
# # with open("E:\Testing_folder\auth and api\API_Handling.js", "rb") as f:
# #     src = f.read()
# # src = bytes(
# #     """let x = 1;
# #     console.log(x);""",
# #     "utf8",
# # )
# # tree = parser.parse(
# #     src
# # )

# # tree = parser.parse(read_callable_byte_offset, encoding="utf8")

# # walked = tree.walk()
# # root_node = tree.root_node
# # print(tree.print_dot_graph)

# def remove_comments_from_js(js_code):
#     """
#     Removes comments from the given JavaScript code using Tree-sitter.
#     """
#     parser = Parser(JS_LANGUAGE)
#     tree = parser.parse(bytes(js_code, "utf8"))
#     root_node = tree.root_node

#     def traverse_and_collect(node):
#         """
#         Recursively traverse the syntax tree and collect non-comment code.
#         """
#         if node.type in ["comment", "ERROR"]:
#             return ""
#         if len(node.children) == 0:
#             return js_code[node.start_byte:node.end_byte]
#         return "".join(traverse_and_collect(child) for child in node.children)

#     return traverse_and_collect(root_node)

# # Example usage
# js_code = """
# // This is a single-line comment
# let x = 1; /* This is a multi-line comment */
# let y= 7;
# console.log(x); // Another comment
# """
# cleaned_code = remove_comments_from_js(js_code)
# print("Code without comments:")
# print(cleaned_code)



