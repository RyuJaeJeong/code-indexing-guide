import tree_sitter_java as tsjava
from tree_sitter import Language, Parser

# 1. 언어 로드 및 파서 초기화
JAVA_LANGUAGE = Language(tsjava.language())
parser = Parser(JAVA_LANGUAGE)


with open("path/to/java_file_path/sample.java", 'r') as f:
    java_code = f.read()
# java_code = """
# package com.example;
#
# public class Calculator {
#
#     /**
#      * 두 수를 더합니다.
#      */
#     public int add(int a, int b) {
#         return a + b;
#     }
#
#     public int subtract(int a, int b) {
#         return a - b;
#     }
# }
# """

tree = parser.parse(bytes(java_code, "utf8"))
root_node = tree.root_node
query_scm = """
(method_declaration
  name: (identifier) @method_name
  body: (block) @method_body
)
"""

query = JAVA_LANGUAGE.query(query_scm)
matches = query.matches(root_node)
source_bytes = bytes(java_code, "utf8")
for pattern_index, match in matches:
    name_nodes = match.get("method_name", [])
    body_nodes = match.get("method_body", [])
    if name_nodes and body_nodes:
        name_node = name_nodes[0]
        body_node = body_nodes[0]
        func_name = source_bytes[name_node.start_byte:name_node.end_byte].decode("utf8")
        func_body = source_bytes[body_node.start_byte:body_node.end_byte].decode("utf8")
        print(f"Function: {func_name}")
        print(f"Body:\n{func_body}\n")
        print("-" * 20)


query_scm = """
(class_declaration
  name: (identifier) @class_name
  body: (class_body) @class_body
)
"""

query = JAVA_LANGUAGE.query(query_scm)
matches = query.matches(tree.root_node)

print("\n--- 클래스 추출 결과 ---")

for pattern_index, match in matches:
    # 딕셔너리 키를 쿼리에서 정의한 이름(@class_name, @class_body)으로 사용
    name_nodes = match.get("class_name", [])
    body_nodes = match.get("class_body", [])

    if name_nodes and body_nodes:
        name_node = name_nodes[0]
        body_node = body_nodes[0]

        class_name = source_bytes[name_node.start_byte:name_node.end_byte].decode("utf8")
        class_body = source_bytes[body_node.start_byte:body_node.end_byte].decode("utf8")

        print(f"Class Name: {class_name}")
        # body는 내용이 길 수 있으니 앞부분만 출력 예시
        print(f"Class Body (Preview):\n{class_body}...")
        print("-" * 20)

