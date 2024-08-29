from fake_useragent import UserAgent


# Формируем headers
def get_headers():
    return {
        "user-agent": str(UserAgent().random),
        "content-type": "application/json",
        "x-requested-with": "XMLHttpRequest",
    }
