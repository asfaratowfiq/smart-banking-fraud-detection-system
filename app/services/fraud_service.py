
import json


def apply_rules(

    normalized_data,

    metadata_data
):

    with open(

        "configs/rules/basic_rules.json",

        "r"

    ) as f:

        rules = json.load(
            f
        )

    findings = []

    score = 0

    salary_slip = None

    bank_statement = None

    # -------------------------
    # Per Document Rules
    # -------------------------

    for file_name, file_data in normalized_data.items():

        metadata = metadata_data.get(

            file_name,

            {}
        )

        combined = {

            **file_data,

            **metadata
        }

        combined[
            "salary_presence"
        ] = (

            combined.get(

                "net_salary"
            )

            or

            combined.get(

                "salary_credit_amount"
            )
        )

        document_type = combined.get(

            "document_type"
        )

        if document_type == "salary_slip":

            salary_slip = combined

        elif document_type == "bank_statement":

            bank_statement = combined

        for rule in rules:

            allowed_documents = rule.get(

                "document_types",

                []
            )

            if (

                allowed_documents

                and

                document_type

                not in allowed_documents
            ):

                continue

            field = rule["field"]

            value = combined.get(

                field
            )

            triggered = False

            if rule["operator"] == "missing":

                triggered = not value

            elif rule["operator"] == "less_than":

                try:

                    triggered = (

                        float(value)

                        <

                        rule["threshold"]
                    )

                except:

                    triggered = False

            elif rule["operator"] == "greater_than":

                try:

                    triggered = (

                        float(value)

                        >

                        rule["threshold"]
                    )

                except:

                    triggered = False

            if triggered:

                findings.append({

                    "rule_id":

                    rule["rule_id"],

                    "message":

                    rule["message"],

                    "severity":

                    rule["severity"]
                })

                score += rule[
                    "weight"
                ]

    # -------------------------
    # Cross Document Rules
    # -------------------------

    if salary_slip and bank_statement:

        salary_amount = salary_slip.get(

            "net_salary"
        )

        bank_salary = bank_statement.get(

            "salary_credit_amount"
        )

        salary_month = salary_slip.get(

            "salary_month"
        )

        statement_month = bank_statement.get(

            "statement_month"
        )

        # CROSS001 Salary Mismatch %

        if salary_amount and bank_salary:

            difference = abs(

                float(salary_amount)

                -

                float(bank_salary)
            )

            difference_percent = (

                difference

                /

                float(salary_amount)

            ) * 100

            if difference_percent > 5:

                findings.append({

                    "rule_id":

                    "CROSS001",

                    "message":

                    "Salary mismatch detected",

                    "severity":

                    "HIGH"
                })

                score += 40

        # CROSS002 Month mismatch

        if (

            salary_month

            and

            statement_month

            and

            salary_month.lower()

            !=

            statement_month.lower()
        ):

            findings.append({

                "rule_id":

                "CROSS002",

                "message":

                "Salary month mismatch",

                "severity":

                "MEDIUM"
            })

            score += 20

        # CROSS003 Missing Salary Credit

        if not bank_salary:

            findings.append({

                "rule_id":

                "CROSS003",

                "message":

                "Salary credit missing in bank statement",

                "severity":

                "HIGH"
            })

            score += 35


        # CROSS004 Invalid Bank Statement

        transaction_count = bank_statement.get(

            "transaction_count",

            0
        )

        if (

            transaction_count < 1

            and

            not bank_salary
        ):

            findings.append({

                "rule_id":

                "CROSS004",

                "message":

                "Incomplete or invalid bank statement detected",

                "severity":

                "HIGH"
            })

            score += 30


        # CROSS005 Invalid Salary Slip

        if not salary_amount:

            findings.append({

                "rule_id":

                "CROSS005",

                "message":

                "Incomplete or invalid salary slip detected",

                "severity":

                "HIGH"
            })

            score += 30


        # FRAUD001 Very High Salary Credit

        if (

            bank_salary

            and

            float(bank_salary) > 250000
        ):

            findings.append({

                "rule_id":

                "FRAUD001",

                "message":

                "Unusually high salary credit",

                "severity":

                "MEDIUM"
            })

            score += 15

        # FRAUD002 Too Many Credits

        transaction_count = bank_statement.get(

            "transaction_count",

            0
        )

        if transaction_count > 200:

            findings.append({

                "rule_id":

                "FRAUD002",

                "message":

                "Very high transaction volume",

                "severity":

                "LOW"
            })

            score += 10

                # -------------------------
    # SAL003 Payroll Validation
    # -------------------------

    if salary_slip:

        gross = salary_slip.get(

            "gross_earnings"
        )

        deductions = salary_slip.get(

            "total_deductions"
        )

        net_salary = salary_slip.get(

            "net_salary"
        )

        if (

            gross is not None

            and

            deductions is not None

            and

            net_salary is not None
        ):

            expected_salary = (

                float(gross)

                -

                float(deductions)
            )

            difference = abs(

                expected_salary

                -

                float(net_salary)
            )

            if difference > 100:

                findings.append({

                    "rule_id": "SAL003",

                    "message": "Payroll arithmetic mismatch detected",

                    "severity": "HIGH"
                })

                score += 40

        # -------------------------
    # BANK001 Balance Validation
    # -------------------------

    if bank_statement:

        opening_balance = bank_statement.get(

            "opening_balance"
        )

        closing_balance = bank_statement.get(

            "closing_balance"
        )

        total_credits = bank_statement.get(

            "total_credits"
        )

        total_debits = bank_statement.get(

            "total_debits"
        )

        if (

            opening_balance is not None

            and

            closing_balance is not None

            and

            total_credits is not None

            and

            total_debits is not None
        ):

            expected_closing = (

                float(opening_balance)

                +

                float(total_credits)

                -

                float(total_debits)
            )

            difference = abs(

                expected_closing

                -

                float(closing_balance)
            )

            if difference > 100:

                findings.append({

                    "rule_id": "BANK001",

                    "message": "Balance reconciliation mismatch detected",

                    "severity": "HIGH"
                })

                score += 40
                
                
    return {

        "score": score,

        "findings": findings
    }
