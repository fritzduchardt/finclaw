from ..social import trump_utils

def register(mcp) -> None:

    @mcp.tool()
    def print_truth_headlines(start_date: str, end_date: str) -> str:
        trump_utils.print_truth_headlines(start_date=start_date, end_date=end_date)
        return "ok"
