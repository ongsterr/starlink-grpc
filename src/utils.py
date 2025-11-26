from src.api import get_all_user_terminals


def get_routers_list():
    user_terminals = get_all_user_terminals()
    user_terminals = [
        {
            "ut_id": ut["userTerminalId"],
            "ut_name": ut["nickname"],
            "router_id": router["routerId"],
            "router_name": router["nickname"],
        }
        for ut in user_terminals["content"]["results"]
        for router in ut["routers"]
    ]
    return user_terminals
