import re

def is_variable(term):
    return isinstance(term, str) and term.islower() and '(' not in term

def parse_literal(lit_str):
    lit_str = lit_str.strip()
    is_pos = True
    if lit_str.startswith('~'):
        is_pos = False
        lit_str = lit_str[1:].strip()

    match = re.match(r'^([A-Za-z0-9_]+)\((.*)\)$', lit_str)
    if not match:
        return (is_pos, lit_str, [])
    pred = match.group(1)
    args = [arg.strip() for arg in match.group(2).split(',') if arg.strip()]
    return (is_pos, pred, args)

def format_literal(lit):
    is_pos, pred, args = lit
    prefix = "" if is_pos else "~"
    if not args:
        return f"{prefix}{pred}"
    return f"{prefix}{pred}({', '.join(args)})"

def format_clause(clause):
    if not clause:
        return "□ (Empty Clause)"
    return " | ".join(format_literal(lit) for lit in sorted(clause))

def to_cnf_clauses(sentence_str, negate=False):
    sentence_str = sentence_str.strip()

    if '=>' in sentence_str:
        parts = sentence_str.split('=>')
        if len(parts) != 2:
            raise ValueError("Invalid rule format: only one '=>' allowed per line.")
        lhs, rhs = parts
        premises = [parse_literal(p) for p in lhs.split('^')]
        conc = parse_literal(rhs)

        cnf_lits = [(not p[0], p[1], tuple(p[2])) for p in premises]
        cnf_lits.append((conc[0], conc[1], tuple(conc[2])))

        if not negate:
            return [frozenset(cnf_lits)]
        else:
            return [frozenset([(not l[0], l[1], l[2])]) for l in cnf_lits]

    lits = [parse_literal(l) for l in sentence_str.split('|')]
    formatted_lits = [(l[0], l[1], tuple(l[2])) for l in lits]

    if not negate:
        return [frozenset(formatted_lits)]
    else:
        return [frozenset([(not l[0], l[1], l[2])]) for l in formatted_lits]

def subst_literal(theta, lit):
    is_pos, pred, args = lit
    new_args = []
    for arg in args:
        while arg in theta:
            arg = theta[arg]
        new_args.append(arg)
    return (is_pos, pred, tuple(new_args))

def subst_clause(theta, clause):
    return frozenset(subst_literal(theta, lit) for lit in clause)

def occurs_check(var, x, theta):
    if var == x:
        return True
    elif is_variable(x) and x in theta:
        return occurs_check(var, theta[x], theta)
    return False

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    elif occurs_check(var, x, theta):
        return None
    else:
        new_theta = theta.copy()
        new_theta[var] = x
        return new_theta

def unify(x, y, theta=None):
    if theta is None:
        theta = {}
    if x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, tuple) and isinstance(y, tuple):
        if len(x) != len(y):
            return None
        for a, b in zip(x, y):
            theta = unify(a, b, theta)
            if theta is None:
                return None
        return theta
    return None

var_counter = 0

def standardize_clause(clause):
    global var_counter
    mapping = {}
    new_lits = []
    for is_pos, pred, args in clause:
        new_args = []
        for arg in args:
            if is_variable(arg):
                if arg not in mapping:
                    var_counter += 1
                    mapping[arg] = f"v_{var_counter}"
                new_args.append(mapping[arg])
            else:
                new_args.append(arg)
        new_lits.append((is_pos, pred, tuple(new_args)))
    return frozenset(new_lits)

def fol_resolve(ci, cj):
    resolvents = set()
    ci_std = standardize_clause(ci)
    cj_std = standardize_clause(cj)

    for l1 in ci_std:
        for l2 in cj_std:
            if l1[0] != l2[0] and l1[1] == l2[1] and len(l1[2]) == len(l2[2]):
                theta = unify(l1[2], l2[2], {})
                if theta is not None:
                    rem_ci = ci_std - {l1}
                    rem_cj = cj_std - {l2}
                    resolvent = subst_clause(theta, rem_ci | rem_cj)
                    resolvents.add(resolvent)
    return resolvents

def fol_resolution(clauses):
    clauses = set(clauses)
    step = 1

    print("\n--- Initial CNF Clauses (KB ∪ {~S}) ---")
    for idx, c in enumerate(clauses, 1):
        print(f"  C{idx}: {format_clause(c)}")

    while True:
        new_clauses = set()
        clause_list = list(clauses)
        n = len(clause_list)

        for i in range(n):
            for j in range(i + 1, n):
                resolvents = fol_resolve(clause_list[i], clause_list[j])
                for res in resolvents:
                    if len(res) == 0:
                        print(f"\n[Step {step}] Resolved ({format_clause(clause_list[i])}) and ({format_clause(clause_list[j])})")
                        print("  => Derived: □ (Empty Clause) — Contradiction Found!")
                        return True
                    if res not in clauses and res not in new_clauses:
                        print(f"[Step {step}] Derived: {format_clause(res)}")
                        new_clauses.add(res)

        if new_clauses.issubset(clauses):
            return False

        clauses |= new_clauses
        step += 1

def main():
    print("=== FOL Resolution Theorem Prover ===")
    print("Syntax Rules:")
    print("  - Variables: lowercase (e.g., x, y)")
    print("  - Constants & Predicates: Capitalized (e.g., West, American(x))")
    print("  - Operators: '~' for NOT, '|' for OR, '^' for AND, '=>' for IMPLIES")
    print("  - Type 'DONE' when finished entering premises.\n")

    all_clauses = []

    while True:
        entry = input("Enter Premise (or DONE): ").strip()
        if entry.upper() == 'DONE':
            break
        if not entry:
            continue
        try:
            all_clauses.extend(to_cnf_clauses(entry, negate=False))
        except ValueError as e:
            print(f"Error: {e}")

    conclusion_str = input("\nEnter Conclusion S to prove: ").strip()
    negated_goal_clauses = to_cnf_clauses(conclusion_str, negate=True)
    all_clauses.extend(negated_goal_clauses)

    proved = fol_resolution(all_clauses)

    print("\n--- Final Result ---")
    if proved:
        print(f"Output: True — Conclusion '{conclusion_str}' FOLLOWS from the premises.")
    else:
        print(f"Output: False — Conclusion '{conclusion_str}' CANNOT be proved (no progress made).")

if __name__ == "__main__":
    main()
