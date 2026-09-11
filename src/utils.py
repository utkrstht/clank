# Line 4's fstring function was generated via generative AI (being Google AI Overview), search/prompt is "<insert function code from commit 3833b6e> How can I make this shorter?"
def create_rejection_message(rejection_reasons):
    template = f"""Hello, your project has the following issues, please fix them for approval:
    {"\n".join(f"- {item}" for item in rejection_reasons)}
    If you have any questions, DM @kaboom or create a ticket in #ask-the-shipwrights. """\

    return template