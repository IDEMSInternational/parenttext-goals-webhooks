def api_version():
    try:
        from parenttext_goals_webhooks._version import version
    except ModuleNotFoundError:
        version = "dev"

    return version
