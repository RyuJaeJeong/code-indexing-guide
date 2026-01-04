import tree_sitter_javascript as tsjs
from tree_sitter import Language, Parser

# 1. 언어 로드 및 파서 초기화 (Java -> JavaScript로 변경)
JS_LANGUAGE = Language(tsjs.language())
parser = Parser(JS_LANGUAGE)

# 테스트용 JS 코드 (Next.js/React 스타일 포함)
with open("path/to/js_file_path/sample.js", 'r') as f:
    js_code = f.read()
# js_code = """
# class Calculator {
#     // 클래스 메서드
#     add(a, b) {
#         return a + b;
#     }
# }
#
# // 일반 함수 선언
# function subtract(a, b) {
#     return a - b;
# }
#
# // 화살표 함수 (변수에 할당)
# const multiply = (a, b) => {
#     return a * b;
# };
#
# // 화살표 함수 (단일 표현식)
# const divide = (a, b) => a / b;
# """

tree = parser.parse(bytes(js_code, "utf8"))
root_node = tree.root_node
source_bytes = bytes(js_code, "utf8")

print("--- 함수 및 메서드 추출 결과 ---")

# ---------------------------------------------------------
# [핵심] JavaScript용 쿼리 (SCM)
# 1. function_declaration: 일반 함수 (function abc() {})
# 2. method_definition: 클래스 내 메서드 (abc() {})
# 3. variable_declarator: 화살표 함수나 익명 함수가 변수에 할당된 경우 (const abc = () => {})
# ---------------------------------------------------------
query_scm_func = """
(function_declaration
  name: (identifier) @func_name
  body: (statement_block) @func_body
)

(method_definition
  name: (property_identifier) @func_name
  body: (statement_block) @func_body
)

(variable_declarator
  name: (identifier) @func_name
  value: [(arrow_function) (function_expression)] @func_full_node
)
"""

query = JS_LANGUAGE.query(query_scm_func)
matches = query.matches(root_node)

for pattern_index, match in matches:
    # 1. 이름 추출
    name_nodes = match.get("func_name", [])

    # 2. 본문 추출
    # (화살표 함수는 body가 없는 경우도 있어서 전체 노드나 value를 잡기도 함)
    body_nodes = match.get("func_body", [])
    full_nodes = match.get("func_full_node", []) # 화살표 함수용

    if name_nodes:
        func_name = source_bytes[name_nodes[0].start_byte:name_nodes[0].end_byte].decode("utf8")

        func_body = ""
        if body_nodes:
            # 일반 함수/메서드의 본문 ({ ... })
            func_body = source_bytes[body_nodes[0].start_byte:body_nodes[0].end_byte].decode("utf8")
        elif full_nodes:
            # 화살표 함수의 전체 정의 ((a,b) => ...)
            func_body = source_bytes[full_nodes[0].start_byte:full_nodes[0].end_byte].decode("utf8")

        print(f"Function Name: {func_name}")
        print(f"Body/Value:\n{func_body}")
        print("-" * 20)