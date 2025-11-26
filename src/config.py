starlink_api_config = {
    "v1": {
        "get_tokens": lambda: {"url": "https://www.starlink.com/api/auth/connect/token", "payload": {}},
        "get_accounts": lambda: {"url": "https://web-api.starlink.com/enterprise/v1/accounts", "payload": {}},
        "get_all_addresses": lambda account_number: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/addresses",
            "payload": {},
        },
        "get_all_router_configs": lambda account_number: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/routers/configs",
            "payload": {},
        },
        "get_router_details": lambda account_number, router_id: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/routers/{router_id}",
            "payload": {},
        },
        "get_tls_configs": lambda account_number: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/routers/tls-configs",
            "payload": {},
        },
        "get_all_service_lines": lambda account_number: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/service-lines",
            "payload": {},
        },
        "get_service_line": lambda account_number, service_line_no: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/service-lines/{service_line_no}",
            "payload": {},
        },
        "get_products": lambda account_number: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/service-lines/available-products",
            "payload": {},
        },
        "get_all_user_terminals": lambda account_number: {
            "url": f"https://web-api.starlink.com/enterprise/v1/account/{account_number}/user-terminals",
            "payload": {},
        },
        "get_account_data_usage": lambda account_number, billing_cycles: {
            "url": f"https://web-api.starlink.com/enterprise/v1/accounts/{account_number}/billing-cycles/query",
            "payload": {"previousBillingCycles": billing_cycles, "activeServiceLinesOnly": True},
        },
        "get_telemetry": lambda account_number, batch_size, max_linger_ms: {
            "url": f"https://web-api.starlink.com/telemetry/stream/v1/telemetry",
            "payload": {"accountNumber": account_number, "batchSize": batch_size, "maxLingerMs": max_linger_ms},
        },
    },
    "v2": {
        "get_tokens": lambda: {"url": "https://www.starlink.com/api/auth/connect/token", "payload": {}},
        "get_accounts": lambda: {"url": "https://starlink.com/api/public/v2/account", "payload": {}},
        "get_all_addresses": lambda _=None: {
            "url": f"https://starlink.com/api/public/v2/addresses",
            "payload": {},
        },
        "get_all_router_configs": lambda _=None: {
            "url": f"https://starlink.com/api/public/v2/routers/configs",
            "payload": {},
        },
        "get_router_details": lambda _=None, router_id=None: {
            "url": f"https://starlink.com/api/public/v2/routers/{router_id}",
            "payload": {},
        },
        "get_all_service_lines": lambda _=None: {
            "url": f"https://starlink.com/api/public/v2/service-lines",
            "payload": {},
        },
        "get_service_line": lambda _=None, service_line_no=None: {
            "url": f"https://starlink.com/api/public/v2/service-lines/{service_line_no}",
            "payload": {},
        },
        "get_products": lambda _=None: {
            "url": f"https://starlink.com/api/public/v2/products",
            "payload": {},
        },
        "get_all_user_terminals": lambda _=None: {
            "url": f"https://starlink.com/api/public/v2/user-terminals",
            "payload": {},
        },
        "get_account_data_usage": lambda service_lines, billing_cycles: {
            "url": f"https://starlink.com/api/public/v2/data-usage/query",
            "payload": {
                "serviceLineNumbers": service_lines,
                "previousBillingCycles": billing_cycles,
                "activeServiceLinesOnly": True,
            },
        },
        "get_telemetry_stream": lambda _=None, batch_size=1000, max_linger_ms=15000: {
            "url": f"https://starlink.com/api/public/v2/telemetry/stream",
            "payload": {"batchSize": batch_size, "maxLingerMs": max_linger_ms},
        },
        "get_telemetry_cached": lambda _=None, include_user_terminals=True, include_routers=True: {
            "url": "https://starlink.com/api/public/v2/telemetry/query",
            "payload": {"includeUserTerminals": include_user_terminals, "includeRouters": include_routers},
        },
    },
}
