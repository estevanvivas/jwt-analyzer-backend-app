from typing import List, Optional, Union
from dataclasses import dataclass
from anytree import Node, RenderTree
from lark import Lark, Tree, Token


__all__ = ['analyze_json_grammar', 'DerivationResult', 'DerivationStep', 'Production']


@dataclass(frozen=True)
class Production:
    source: str
    target: str

    def __str__(self) -> str:
        return f"{self.source} -> {self.target}"


@dataclass(frozen=True)
class DerivationStep:
    production: Production
    result: str


@dataclass(frozen=True)
class DerivationResult:
    tree: str
    steps: List[DerivationStep]

    def format_derivation_steps(self) -> str:
        lines = [f"0. {self.steps[0].production.source if self.steps else ''}"]

        for i, step in enumerate(self.steps, 1):
            lines.append(f"{i}. {step.result}")
            lines.append(f"   Usando: {step.production}")

        return "\n".join(lines)


_JSON_GRAMMAR = r"""
object        : LBRACE members_opt RBRACE
members_opt   : members?
members       : pair (COMMA members)?
pair          : key COLON value

value         : string
              | number
              | object
              | array
              | boolean
              | null

array         : LBRACK elements_opt RBRACK
elements_opt  : elements?
elements      : value (COMMA elements)?

string        : ESCAPED_STRING
number        : SIGNED_NUMBER
boolean       : TRUE | FALSE
null          : NULL
key           : ESCAPED_STRING

LBRACE        : "{"
RBRACE        : "}"
LBRACK        : "["
RBRACK        : "]"
COLON         : ":"
COMMA         : ","
TRUE          : "true"
FALSE         : "false"
NULL          : "null"

%import common.ESCAPED_STRING
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS
"""

_EPSILON = "ε"

_parser = Lark(_JSON_GRAMMAR, start="object", parser="lalr")


def analyze_json_grammar(json_string: str) -> DerivationResult:
    lark_tree = _parser.parse(json_string)
    anytree_root = _lark_to_anytree(lark_tree)

    return DerivationResult(
        tree=_format_tree(anytree_root),
        steps=_trace_derivation(lark_tree)
    )


def _format_tree(root: Node) -> str:
    lines = []
    for pre, _, node in RenderTree(root):
        lines.append(f"{pre}{node.name}")
    return "\n".join(lines)


def _lark_to_anytree(lark_node: Union[Tree, Token]) -> Optional[Node]:
    if isinstance(lark_node, Tree):
        node = Node(lark_node.data)
        for child in lark_node.children:
            child_node = _lark_to_anytree(child)
            if child_node is not None:
                child_node.parent = node
        return node
    elif isinstance(lark_node, Token):
        return Node(str(lark_node))
    return None


def _get_grammar_rules(tree: Tree) -> List[Production]:
    productions = []
    _collect_productions(tree, productions)
    return productions


def _collect_productions(node: Tree, productions: List[Production]) -> None:
    if not isinstance(node, Tree):
        return

    source = node.data
    target_parts = []

    for child in node.children:
        if isinstance(child, Tree):
            target_parts.append(child.data)
        elif isinstance(child, Token):
            target_parts.append(str(child))

    right_side = " ".join(target_parts) if target_parts else _EPSILON
    productions.append(Production(source, right_side))

    for child in node.children:
        if isinstance(child, Tree):
            _collect_productions(child, productions)


def _trace_derivation(tree: Tree) -> List[DerivationStep]:
    steps = []
    current_string = [tree.data]

    productions = _get_grammar_rules(tree)

    for prod in productions:
        new_string = []
        replaced = False

        for symbol in current_string:
            if symbol == prod.source and not replaced:
                if prod.target != _EPSILON:
                    new_string.extend(prod.target.split())
                replaced = True
            else:
                new_string.append(symbol)

        current_string = new_string
        steps.append(DerivationStep(prod, " ".join(current_string)))

    return steps
