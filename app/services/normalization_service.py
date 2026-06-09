import re

def normalize_text(
    extracted_data
):

    output = {}

    # -------------------------
    # Structured JSON Input
    # -------------------------

    if isinstance(

        extracted_data,

        dict
    ):

        # -------------------------
        # Salary Slip JSON
        # -------------------------

        if (

            "earnings" in extracted_data

            or

            "net_salary" in extracted_data
        ):

            net_salary = extracted_data.get(

                "net_salary",

                {}
            )

            output[
                "document_type"
            ] = "salary_slip"

            output[
                "net_salary"
            ] = net_salary.get(

                "amount"
            )

            output[
                "salary_month"
            ] = extracted_data.get(

                "month"
            )

            output[
                "transaction_count"
            ] = 0

            return output

        # -------------------------
        # Bank JSON
        # -------------------------

        transactions = extracted_data.get(

            "transactions",

            []
        )

        salary_credit = 0

        for txn in transactions:

            description = str(

                txn.get(

                    "description",

                    ""
                )

            ).lower()

            amount = txn.get(

                "amount",

                0
            )

            if (

                "salary" in description

                or

                "payroll" in description
            ):

                salary_credit = max(

                    salary_credit,

                    amount
                )

        output[
            "document_type"
        ] = "bank_statement"

        output[
            "salary_credit_amount"
        ] = salary_credit

        output[
            "transaction_count"
        ] = len(
            transactions
        )

        output[
            "statement_month"
        ] = extracted_data.get(

            "month"
        )

        return output

    # -------------------------
    # TEXT FALLBACK
    # -------------------------

    text_lower = extracted_data.lower()

    bank_keywords = [

        "opening balance",

        "closing balance",

        "statement period",

        "account statement",

        "upi",

        "imps",

        "neft",

        "withdrawal",

        "total credits"
    ]

    bank_matches = sum(

        keyword in text_lower

        for keyword in bank_keywords
    )

    is_bank_statement = (

        bank_matches >= 2
    )

    # -------------------------
    # BANK TEXT
    # -------------------------

    if is_bank_statement:

        output[
            "document_type"
        ] = "bank_statement"

        output[
            "transaction_count"
        ] = text_lower.count(

            "credit"
        )

        salary_credit = None

        lines = text_lower.splitlines()

        for line in lines:

            if (

                "salary" in line

                or

                "payroll" in line
            ):

                amounts = re.findall(

                    r'(\d{1,3}(?:,\d{2,3})*\.\d{2})',

                    line
                )

                if amounts:

                    valid_amounts = []

                    for amount in amounts:

                        try:

                            numeric = float(

                                amount.replace(

                                    ",",

                                    ""
                                )
                            )

                            if numeric > 10000:

                                valid_amounts.append(

                                    numeric
                                )

                        except:

                            pass

                    if valid_amounts:

                        salary_credit = valid_amounts[0]

                        break

        if salary_credit is None:

            neft_match = re.search(

                r'neft.*?(\d{1,3}(?:,\d{2,3})*\.\d{2})',

                text_lower,

                re.IGNORECASE
            )

            if neft_match:

                try:

                    salary_credit = float(

                        neft_match.group(1)

                        .replace(",", "")
                    )

                except:

                    pass

        if salary_credit:

            output[
                "salary_credit_amount"
            ] = salary_credit

        month_match = re.search(

            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',

            text_lower,

            re.IGNORECASE
        )

        if month_match:

            output[
                "statement_month"
            ] = month_match.group()

        # -------------------------
        # Opening Balance
        # -------------------------

        opening_match = re.search(

            r'opening balance.*?([\d,]+\.\d{2})',

            text_lower,

            re.IGNORECASE
        )

        if opening_match:

            try:

                output[
                    "opening_balance"
                ] = float(

                    opening_match.group(1)

                    .replace(",", "")
                )

            except:

                pass

        # -------------------------
        # Closing Balance
        # -------------------------

        closing_match = re.search(

            r'closing balance.*?([\d,]+\.\d{2})',

            text_lower,

            re.IGNORECASE
        )

        if closing_match:

            try:

                output[
                    "closing_balance"
                ] = float(

                    closing_match.group(1)

                    .replace(",", "")
                )

            except:

                pass

        # -------------------------
        # Total Credits
        # -------------------------

        credits_match = re.search(

            r'total credits.*?([\d,]+\.\d{2})',

            text_lower,

            re.IGNORECASE
        )

        if credits_match:

            try:

                output[
                    "total_credits"
                ] = float(

                    credits_match.group(1)

                    .replace(",", "")
                )

            except:

                pass

        # -------------------------
        # Total Debits
        # -------------------------

        debits_match = re.search(

            r'total debits.*?([\d,]+\.\d{2})',

            text_lower,

            re.IGNORECASE
        )

        if debits_match:

            try:

                output[
                    "total_debits"
                ] = float(

                    debits_match.group(1)

                    .replace(",", "")
                )

            except:

                pass

        print("BANK NORMALIZED:", output)

        return output
    # -------------------------
    # SALARY TEXT
    # -------------------------

    output[
        "document_type"
    ] = "salary_slip"

    month_match = re.search(

        r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',

        text_lower,

        re.IGNORECASE
    )

    if month_match:

        output[
            "salary_month"
        ] = month_match.group()

    salary_patterns = [

        r'net salary payable.*?(\d{1,3}(?:,\d{2,3})*)',

        r'net salary.*?(\d{1,3}(?:,\d{2,3})*)',

        r'payable.*?(\d{1,3}(?:,\d{2,3})*)'
    ]

    salary_amount = None

    for pattern in salary_patterns:

        match = re.search(

            pattern,

            text_lower,

            re.IGNORECASE
        )

        if match:

            try:

                salary_amount = int(

                    match.group(1)

                    .replace(",", "")
                )

                break

            except:

                pass

    if salary_amount:

        output[
            "net_salary"
        ] = salary_amount

    # -------------------------
    # Gross Earnings
    # -------------------------

    gross_match = re.search(

        r'gross earnings.*?(\d[\d,]*)',

        text_lower,

        re.IGNORECASE
    )

    if gross_match:

        try:

            output[
                "gross_earnings"
            ] = int(

                gross_match.group(1)

                .replace(",", "")
            )

        except:

            pass

    # -------------------------
    # Total Deductions
    # -------------------------

    deduction_match = re.search(

        r'total deductions.*?(\d[\d,]*)',

        text_lower,

        re.IGNORECASE
    )

    if deduction_match:

        try:

            output[
                "total_deductions"
            ] = int(

                deduction_match.group(1)

                .replace(",", "")
            )

        except:

            pass

    output[
        "transaction_count"
    ] = 0

    return output
