import os
import ply.lex as lex
import ply.yacc as yacc

from core.object import *
from ..Verilog import *
from modules.LogicGate import *

# =====================================================================
# 1. PURE PYTHON VERILOG LEXER & PARSER (PLY)
# =====================================================================

tokens = (
    'MODULE', 'ENDMODULE', 'INPUT', 'OUTPUT', 'WIRE', 'REG', 'ASSIGN', 'ALWAYS',
    'POSEDGE', 'NEGEDGE', 'OR_KEYWORD', 'IF', 'ELSE', 'BEGIN', 'END',
    'IDENTIFIER', 'NUMBER',
    'AND_OP', 'OR_OP', 'XOR_OP', 'NOT_OP',
    'ASSIGN_LE', 'ASSIGN_EQ',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COLON', 'SEMICOLON', 'COMMA', 'AT'
)

t_AND_OP     = r'&'
t_OR_OP      = r'\|'
t_XOR_OP     = r'\^'
t_NOT_OP     = r'~'
t_ASSIGN_LE  = r'<='
t_ASSIGN_EQ  = r'='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_COLON      = r':'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_AT         = r'@'

reserved = {
    'module': 'MODULE', 'endmodule': 'ENDMODULE', 'input': 'INPUT', 'output': 'OUTPUT',
    'wire': 'WIRE', 'reg': 'REG', 'assign': 'ASSIGN', 'always': 'ALWAYS',
    'posedge': 'POSEDGE', 'negedge': 'NEGEDGE', 'or': 'OR_KEYWORD', 'if': 'IF',
    'else': 'ELSE', 'begin': 'BEGIN', 'end': 'END'
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r"(\d+'[bBoOdDhH][0-9a-fA-F_]+)|\d+"
    return t

t_ignore = ' \t\r\n'

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass

def t_error(t):
    t.lexer.skip(1)

class ASTNode:
    def __init__(self, type, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)

def p_module(p):
    '''module : MODULE IDENTIFIER LPAREN port_list RPAREN SEMICOLON items ENDMODULE'''
    p[0] = ASTNode('Module', name=p[2], ports=p[4], items=p[7])

def p_port_list(p):
    '''port_list : inline_port
                 | port_list COMMA inline_port'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_inline_port(p):
    '''inline_port : decl_type net_type range IDENTIFIER
                   | decl_type net_type IDENTIFIER
                   | decl_type range IDENTIFIER
                   | decl_type IDENTIFIER
                   | IDENTIFIER'''
    if len(p) == 5:
        p[0] = ASTNode('Decl', direction=p[1], net_type=p[2], width=p[3], name=p[4])
    elif len(p) == 4:
        if isinstance(p[2], tuple):
            p[0] = ASTNode('Decl', direction=p[1], net_type=None, width=p[2], name=p[3])
        else:
            p[0] = ASTNode('Decl', direction=p[1], net_type=p[2], width=None, name=p[3])
    elif len(p) == 3:
        p[0] = ASTNode('Decl', direction=p[1], net_type=None, width=None, name=p[2])
    else:
        p[0] = p[1]

def p_net_type(p):
    '''net_type : WIRE
                | REG'''
    p[0] = p[1]

def p_items(p):
    '''items : item
             | items item'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + ([p[2]] if p[2] else [])

def p_item(p):
    '''item : decl_item
            | assign_item
            | always_item'''
    p[0] = p[1]

def p_decl_item(p):
    '''decl_item : decl_type net_type range IDENTIFIER SEMICOLON
                 | decl_type range IDENTIFIER SEMICOLON
                 | decl_type IDENTIFIER SEMICOLON
                 | net_type range IDENTIFIER SEMICOLON
                 | net_type IDENTIFIER SEMICOLON'''
    if len(p) == 6:
        p[0] = ASTNode('Decl', direction=p[1], net_type=p[2], width=p[3], name=p[4])
    elif len(p) == 5:
        p[0] = ASTNode('Decl', direction=p[1], net_type=None, width=p[2], name=p[3])
    elif len(p) == 4:
        p[0] = ASTNode('Decl', direction=p[1], net_type=None, width=None, name=p[2])

def p_decl_type(p):
    '''decl_type : INPUT
                 | OUTPUT'''
    p[0] = p[1]

def p_range(p):
    '''range : LBRACKET NUMBER COLON NUMBER RBRACKET'''
    p[0] = (int(p[2]), int(p[4]))

def p_assign_item(p):
    '''assign_item : ASSIGN IDENTIFIER ASSIGN_EQ expr SEMICOLON'''
    p[0] = ASTNode('Assign', lhs=p[2], rhs=p[4])

def p_always_item(p):
    '''always_item : ALWAYS AT LPAREN sens_list RPAREN stmt'''
    p[0] = ASTNode('Always', sens=p[4], stmt=p[6])

def p_sens_list(p):
    '''sens_list : sens_event
                 | sens_list OR_KEYWORD sens_event
                 | sens_list COMMA sens_event'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_sens_event(p):
    '''sens_event : POSEDGE IDENTIFIER
                  | NEGEDGE IDENTIFIER
                  | IDENTIFIER'''
    p[0] = (p[1], p[2]) if len(p) == 3 else ('any', p[1])

def p_stmt(p):
    '''stmt : BEGIN stmt_list END
            | nonblock_stmt
            | if_stmt'''
    if len(p) == 4:
        p[0] = ASTNode('Block', stmts=p[2])
    else:
        p[0] = p[1]

def p_stmt_list(p):
    '''stmt_list : stmt
                 | stmt_list stmt'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    else:
        p[0] = p[1] + ([p[2]] if p[2] else [])

def p_nonblock_stmt(p):
    '''nonblock_stmt : IDENTIFIER ASSIGN_LE expr SEMICOLON'''
    p[0] = ASTNode('Nonblocking', lhs=p[1], rhs=p[3])

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expr RPAREN stmt ELSE stmt
               | IF LPAREN expr RPAREN stmt'''
    if len(p) == 8:
        p[0] = ASTNode('If', cond=p[3], then_branch=p[5], else_branch=p[7])
    else:
        p[0] = ASTNode('If', cond=p[3], then_branch=p[5], else_branch=None)

precedence = (
    ('left', 'OR_OP'),
    ('left', 'XOR_OP'),
    ('left', 'AND_OP'),
    ('right', 'NOT_OP'),
)

def p_expr_binop(p):
    '''expr : expr AND_OP expr
            | expr OR_OP expr
            | expr XOR_OP expr'''
    p[0] = ASTNode('BinOp', op=p[2], left=p[1], right=p[3])

def p_expr_unop(p):
    '''expr : NOT_OP expr'''
    p[0] = ASTNode('UnaryOp', op=p[1], operand=p[2])

def p_expr_primary(p):
    '''expr : IDENTIFIER
            | NUMBER
            | LPAREN expr RPAREN'''
    if len(p) == 2:
        p[0] = ASTNode('Var', name=p[1])
    else:
        p[0] = p[2]

def p_error(p):
    pass

lexer = lex.lex()
parser = yacc.yacc(write_tables=False, debug=False)


# =====================================================================
# 2. GATE-LEVEL DFF BUILDER & COMPILER
# =====================================================================

def build_pure_gate_dff(Name, io_d, io_clk, io_clr, io_q):
    n1 = NANDGate(f"{Name}_N1")
    n2 = NANDGate(f"{Name}_N2")
    n3 = NANDGate(f"{Name}_N3")
    n4 = NANDGate(f"{Name}_N4")
    n5 = NANDGate(f"{Name}_N5")
    n6 = NANDGate(f"{Name}_N6")
    inv_clr = NOTGate(f"{Name}_clr_inv")
    clr_and = ANDGate(f"{Name}_clr_and")

    io_clr >> inv_clr.IO["A"]

    n4.IO["OUT"] >> n1.IO["A"]
    n2.IO["OUT"] >> n1.IO["B"]

    n1.IO["OUT"] >> n2.IO["A"]
    io_clk >> n2.IO["B"]

    n2.IO["OUT"] >> n3.IO["A"]
    io_clk >> n3.IO["B"]

    n3.IO["OUT"] >> n4.IO["A"]
    io_d >> n4.IO["B"]

    n2.IO["OUT"] >> n5.IO["A"]
    n6.IO["OUT"] >> n5.IO["B"]

    n5.IO["OUT"] >> n6.IO["A"]
    n3.IO["OUT"] >> n6.IO["B"]

    inv_clr.IO["OUT"] >> clr_and.IO["A"]
    n5.IO["OUT"] >> clr_and.IO["B"]

    clr_and.IO["OUT"] >> io_q

    return [n1, n2, n3, n4, n5, n6, inv_clr, clr_and]


class VerilogGateLevelCompiler:
    def __init__(self):
        self.ModuleIO = {}
        self.internal_wires = {}
        self.gate_counter = 0

    def _get_or_create_wire(self, wire_name):
        if wire_name in self.ModuleIO:
            return self.ModuleIO[wire_name]
        if wire_name in self.internal_wires:
            return self.internal_wires[wire_name]
        new_internal_io = IO(f"internal_wire_{wire_name}")
        self.internal_wires[wire_name] = new_internal_io
        return new_internal_io

    def _get_next_gate_name(self, block_prefix, gate_type):
        self.gate_counter += 1
        return f"{block_prefix}_{gate_type}_{self.gate_counter}"

    def parse_module_io_header(self, mod_node):
        all_decls = [p for p in mod_node.ports if isinstance(p, ASTNode) and p.type == 'Decl']
        all_decls.extend([i for i in mod_node.items if isinstance(i, ASTNode) and i.type == 'Decl'])

        for item in all_decls:
            if item.direction in ('input', 'output'):
                port_name = item.name
                if item.width:
                    msb, lsb = item.width
                    start, end = min(msb, lsb), max(msb, lsb) + 1
                    for i in range(start, end):
                        bit_name = f"{port_name}_{i}"
                        if bit_name not in self.ModuleIO:
                            self.ModuleIO[bit_name] = IO(bit_name)
                            print(f"[ModuleIO Bus Assign] Assigned Pin: {bit_name}")
                else:
                    if port_name not in self.ModuleIO:
                        self.ModuleIO[port_name] = IO(port_name)
                        print(f"[ModuleIO Scalar Assign] Assigned Pin: {port_name}")

    def compile_assign_node(self, assign_node):
        lhs_text = assign_node.lhs
        is_bus = f"{lhs_text}_0" in self.ModuleIO or f"internal_wire_{lhs_text}_0" in self.internal_wires
        gate_list = []

        if is_bus:
            block_name = f"AssignBlock_Bus_{lhs_text}"

            for i in range(64):
                bit_lhs = f"{lhs_text}_{i}"
                if bit_lhs not in self.ModuleIO and f"internal_wire_{bit_lhs}" not in self.internal_wires:
                    if i == 0:
                        continue
                    break

                lhs_io = self._get_or_create_wire(bit_lhs)
                final_rhs_io = self._parse_expression(assign_node.rhs, gate_list, block_name, bit_index=i)
                final_rhs_io >> lhs_io

            return VerilogBlock(Name=block_name, ComponentArray=gate_list)
        else:
            block_name = f"AssignBlock_{lhs_text}"
            lhs_io = self._get_or_create_wire(lhs_text)

            final_rhs_io = self._parse_expression(assign_node.rhs, gate_list, block_name, bit_index=None)
            final_rhs_io >> lhs_io
            return VerilogBlock(Name=block_name, ComponentArray=gate_list)

    def compile_always_node(self, always_node):
        sens_signals = [sig for edge, sig in always_node.sens if edge in ('posedge', 'negedge')]
        
        # 1. Extract all top-level 'if' conditions inside the block body
        async_cond_signals = self._extract_top_if_conditions(always_node.stmt)

        clk_io = None
        rst_io = None

        # 2. Assign roles purely based on AST structure
        for sig in sens_signals:
            sig_io = self._get_or_create_wire(sig)
            if sig in async_cond_signals:
                rst_io = sig_io  # It's an Async Reset because it guards an 'if' branch
            elif clk_io is None:
                clk_io = sig_io  # It's the Clock trigger

        # Fallback for synchronous circuits (no async reset in sensitivity list)
        if rst_io is None:
            rst_io = self._get_or_create_wire("unused_rst")
            rst_io.Value = 0

        block_name = f"AlwaysBlock_{clk_io.Name if clk_io else 'comb'}"
        gate_list = []
        self._parse_sequential_statement(always_node.stmt, gate_list, clk_io, rst_io, current_cond=None)
        return VerilogBlock(Name=block_name, ComponentArray=gate_list)

    def _extract_top_if_conditions(self, stmt):
        """Recursively inspects the AST body to find signals used in reset 'if' guards."""
        cond_signals = set()
        if stmt is None:
            return cond_signals

        if stmt.type == 'Block':
            for sub_stmt in stmt.stmts:
                cond_signals.update(self._extract_top_if_conditions(sub_stmt))
        elif stmt.type == 'If':
            # Extract identifier name from condition AST node
            if stmt.cond.type == 'Var':
                cond_signals.add(stmt.cond.name)
            # Check nested else-if branches
            if stmt.else_branch and stmt.else_branch.type == 'If':
                cond_signals.update(self._extract_top_if_conditions(stmt.else_branch))

        return cond_signals
        clk_io = None
        rst_io = None

        for edge_type, sig_name in always_node.sens:
            sig_io = self._get_or_create_wire(sig_name)
            if edge_type in ('posedge', 'negedge') and clk_io is None:
                clk_io = sig_io
            else:
                rst_io = sig_io

        if rst_io is None and clk_io is not None:
            rst_io = self._get_or_create_wire("unused_rst")

        block_name = f"AlwaysBlock_{clk_io.Name if clk_io else 'comb'}"
        gate_list = []
        self._parse_sequential_statement(always_node.stmt, gate_list, clk_io, rst_io, current_cond=None)
        return VerilogBlock(Name=block_name, ComponentArray=gate_list)

    def _parse_sequential_statement(self, stmt, gate_list, clk_io, rst_io, current_cond=None):
        if stmt is None:
            return

        if stmt.type == 'Block':
            for sub_stmt in stmt.stmts:
                self._parse_sequential_statement(sub_stmt, gate_list, clk_io, rst_io, current_cond)

        elif stmt.type == 'If':
            # Handle enable/condition signals inside sequential blocks
            cond_io = self._parse_expression(stmt.cond, gate_list, "Cond")
            if stmt.then_branch:
                self._parse_sequential_statement(stmt.then_branch, gate_list, clk_io, rst_io, current_cond=cond_io)
            if stmt.else_branch:
                self._parse_sequential_statement(stmt.else_branch, gate_list, clk_io, rst_io, current_cond=None)

        elif stmt.type == 'Nonblocking':
            lhs_var = stmt.lhs
            rhs_var = stmt.rhs.name if stmt.rhs.type == 'Var' else str(stmt.rhs)

            if "b0" not in rhs_var and rhs_var != "0":
                is_bus = f"{lhs_var}_0" in self.ModuleIO or f"internal_wire_{lhs_var}_0" in self.internal_wires
                if is_bus:
                    for i in range(64):
                        bit_lhs = f"{lhs_var}_{i}"
                        bit_rhs = f"{rhs_var}_{i}"
                        if bit_lhs not in self.ModuleIO and f"internal_wire_{bit_lhs}" not in self.internal_wires:
                            break
                        
                        q_io = self._get_or_create_wire(bit_lhs)
                        d_io = self._get_or_create_wire(bit_rhs)

                        # Wire through conditional enable gate if en is specified
                        if current_cond is not None:
                            en_and = ANDGate(f"Enable_AND_{bit_lhs}")
                            d_io >> en_and.IO["A"]
                            current_cond >> en_and.IO["B"]
                            d_io = en_and.IO["OUT"]
                            gate_list.append(en_and)

                        print(f"[Sequential Synthesis] Mapping Bit-Vector DFF: {bit_lhs} <= {bit_rhs}")
                        dff_net = build_pure_gate_dff(f"DFF_{bit_lhs}", d_io, clk_io, rst_io, q_io)
                        gate_list.extend(dff_net)
                else:
                    q_io = self._get_or_create_wire(lhs_var)
                    d_io = self._get_or_create_wire(rhs_var)

                    if current_cond is not None:
                        en_and = ANDGate(f"Enable_AND_{lhs_var}")
                        d_io >> en_and.IO["A"]
                        current_cond >> en_and.IO["B"]
                        d_io = en_and.IO["OUT"]
                        gate_list.append(en_and)

                    print(f"[Sequential Synthesis] Mapping Scalar DFF: {lhs_var} <= {rhs_var}")
                    dff_net = build_pure_gate_dff(f"DFF_{lhs_var}", d_io, clk_io, rst_io, q_io)
                    gate_list.extend(dff_net)

    def _parse_expression(self, expr, gate_list, block_prefix, bit_index=None):
        if expr.type == 'Var':
            var_name = f"{expr.name}_{bit_index}" if bit_index is not None else expr.name
            return self._get_or_create_wire(var_name)

        elif expr.type == 'BinOp':
            left_io = self._parse_expression(expr.left, gate_list, block_prefix, bit_index)
            right_io = self._parse_expression(expr.right, gate_list, block_prefix, bit_index)

            suffix = f"_{bit_index}" if bit_index is not None else ""
            gate_map = {'&': (ANDGate, "AND"), '|': (ORGate, "OR"), '^': (XORGate, "XOR")}
            gate_cls, gate_type = gate_map[expr.op]

            gate = gate_cls(self._get_next_gate_name(f"{block_prefix}{suffix}", gate_type))
            left_io >> gate.IO["A"]
            right_io >> gate.IO["B"]
            gate_list.append(gate)
            return gate.IO["OUT"]

        elif expr.type == 'UnaryOp' and expr.op == '~':
            operand_io = self._parse_expression(expr.operand, gate_list, block_prefix, bit_index)
            suffix = f"_{bit_index}" if bit_index is not None else ""
            gate = NOTGate(self._get_next_gate_name(f"{block_prefix}{suffix}", "NOT"))
            operand_io >> gate.IO["A"]
            gate_list.append(gate)
            return gate.IO["OUT"]

        raise TypeError(f"Unsupported AST node expression: {expr.type}")


def compile_verilog_file_to_object(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Verilog File Not Found: {file_path}")

    with open(file_path, 'r') as f:
        code = f.read()

    mod_ast = parser.parse(code)
    if not mod_ast:
        raise ValueError("Failed to parse Verilog module")

    compiler = VerilogGateLevelCompiler()
    compiler.parse_module_io_header(mod_ast)
    compiled_blocks = []

    for item in mod_ast.items:
        if item.type == 'Assign':
            block = compiler.compile_assign_node(item)
            if block:
                compiled_blocks.append(block)
        elif item.type == 'Always':
            block = compiler.compile_always_node(item)
            if block:
                compiled_blocks.append(block)

    return VerilogModule(
        Name=mod_ast.name,
        PinOutIOs=compiler.ModuleIO,
        BlockArray=compiled_blocks
    )