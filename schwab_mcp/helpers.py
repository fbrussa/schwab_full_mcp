import httpx


def unwrap(response: httpx.Response) -> dict | list | str:
    """Extract JSON from a schwab-py response, raising on HTTP errors."""
    if response.status_code == httpx.codes.OK:
        return response.json()
    if response.status_code == httpx.codes.CREATED:
        order_id = None
        location = response.headers.get("Location", "")
        if location:
            order_id = location.rsplit("/", 1)[-1]
        return {"status": "created", "order_id": order_id}
    if response.status_code == httpx.codes.NO_CONTENT:
        return {"status": "success"}
    raise RuntimeError(
        f"Schwab API error {response.status_code}: {response.text}"
    )
