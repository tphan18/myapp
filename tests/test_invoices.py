import pytest

test_400_data = [
    True,
    "a",
    "",
    {},
    [],
    [{"units": 1, "description": "foo"}],
    [{"unit": 1, "description": "foo", "amount": 1}],
    [{"units": 1, "description": 123, "amount": 1}],
    [{"units": 1, "description": "foo", "amount": "123"}],
    [{"units": -1, "description": "foo", "amount": 1}],
]


@pytest.fixture
def invoice(client):
    """Return a new invoice."""
    response = client.post(
        "/v1/invoices", json=[{"units": 1, "description": "foo", "amount": 1}]
    )

    return response.json


def test_create_invoice_200(client):
    """Test that the create invoice endpoint returns a 200."""
    response = client.post(
        "/v1/invoices", json=[{"units": 1, "description": "foo", "amount": 1}]
    )

    assert response.status_code == 200
    assert "id" in response.json
    assert "invoice_date" in response.json
    assert "invoice_items" in response.json
    assert response.json["invoice_items"][0]["description"] == "foo"
    assert response.json["invoice_items"][0]["amount"] == 1
    assert response.json["invoice_items"][0]["units"] == 1


@pytest.mark.parametrize("test_input", test_400_data)
def test_create_invoice_400(client, test_input):
    """Test that the create invoice endpoint returns a 400."""
    response = client.post("/v1/invoices", json=test_input)

    assert response.status_code == 400
    assert response.json == {"error": "Invalid JSON payload"}


def test_create_invoice_415(client):
    """Test that the create invoice endpoint returns a 415."""
    response = client.post("/v1/invoices", data="")

    assert response.status_code == 415
    assert response.json == {
        "error": "Invalid Content-Type header, should be application/json"
    }


def test_get_invoices_200_empty(client):
    """Test that the get invoices endpoint returns a 200."""
    response = client.get("/v1/invoices")

    assert response.status_code == 200
    assert "invoices" in response.json
    assert response.json["invoices"] == []


def test_get_invoices_200(client, invoice):
    """Test that the get invoices endpoint returns a 200."""
    response = client.get("/v1/invoices")

    assert response.status_code == 200
    assert response.json["invoices"][0]["id"] == invoice["id"]
    assert response.json["invoices"][0]["invoice_date"] == invoice["invoice_date"]


def test_get_invoice_200(client, invoice):
    """Test that the get invoice endpoint returns a 200."""
    response = client.get(f"/v1/invoices/{invoice['id']}")

    assert response.status_code == 200
    assert response.json["id"] == invoice["id"]
    assert response.json["invoice_date"] == invoice["invoice_date"]
    assert len(response.json["invoice_items"]) == 1


def test_get_invoice_404(client):
    """Test that the get invoice endpoint returns a 404."""
    response = client.get("/v1/invoices/123")

    assert response.status_code == 404
    assert response.json == {"error": "Not found"}


def test_add_invoice_items_200(client, invoice):
    """Test that the add invoice items endpoint returns a 200."""
    response = client.post(
        f"/v1/invoices/{invoice['id']}",
        json=[{"units": 2, "description": "bar", "amount": 1.1}],
    )

    assert response.status_code == 200
    assert len(response.json["invoice_items"]) == 2


def test_add_invoice_items_404(client):
    """Test that the add invoice items endpoint returns a 404."""
    response = client.post(
        "/v1/invoices/123", json=[{"units": 2, "description": "bar", "amount": 1.1}]
    )

    assert response.status_code == 404
    assert response.json == {"error": "Not found"}


@pytest.mark.parametrize("test_input", test_400_data)
def test_add_invoice_items_400(client, invoice, test_input):
    """Test that the add invoice items endpoint returns a 400."""
    response = client.post(
        f"/v1/invoices/{invoice['id']}",
        json=test_input,
    )

    assert response.status_code == 400
    assert response.json == {"error": "Invalid JSON payload"}


def test_add_invoice_items_415(client, invoice):
    """Test that the add invoice items endpoint returns a 415."""
    response = client.post(f"/v1/invoices/{invoice['id']}", data="")

    assert response.status_code == 415
    assert response.json == {
        "error": "Invalid Content-Type header, should be application/json"
    }


def test_invalid_json_payload(client):
    """Test invalid JSON payload."""
    response = client.post(
        "/v1/invoices", data="", headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400
    assert response.json == {"error": "Invalid JSON payload"}
