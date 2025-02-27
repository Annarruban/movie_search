def validate_top_args(args: list[str]) -> None:
    constants = {"keyword", "category", "year",
                 "language", "length", "actor"}
    if not set(args).issubset(constants):
        s = {'\n'.join(constants)}
        raise Exception(f"""Please search by the following values:
{s}""")
