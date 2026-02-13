import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post("/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_fail(client):
    response = await client.post("/auth/login", json={
        "username": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_product_as_admin(client, admin_token):
    response = await client.post(
        "/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Laptop",
            "price": 1000,
            "quantity": 5,
            "min_stock": 2
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Laptop"


@pytest.mark.asyncio
async def test_create_product_as_user_forbidden(client, user_token):
    response = await client.post(
        "/products",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "name": "Mouse",
            "price": 50,
            "quantity": 10,
            "min_stock": 2
        }
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_products_requires_auth(client):
    response = await client.get("/products")
    assert response.status_code == 403 or response.status_code == 401


@pytest.mark.asyncio
async def test_adjust_inventory(client, admin_token):
 
    create = await client.post(
        "/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Keyboard",
            "price": 100,
            "quantity": 10,
            "min_stock": 3
        }
    )

    product_id = create.json()["id"]

    adjust = await client.post(
        "/inventory/adjust",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "product_id": product_id,
            "adjustment": -2,
            "reason": "Sold items"
        }
    )

    assert adjust.status_code == 200
    assert adjust.json()["new_quantity"] == 8

@pytest.mark.asyncio
async def test_low_stock_logic_bug(client, admin_token):
    # crear producto con poco stock
    await client.post(
        "/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Test",
            "price": 100,
            "quantity": 2,
            "min_stock": 5
        }
    )

    response = await client.get(
        "/inventory/low-stock",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    data = response.json()
    assert len(data) == 1

#--
@pytest.mark.asyncio
async def test_inventory_value_bug(client, admin_token):
    await client.post(
        "/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "A", "price": 10, "quantity": 2}
    )

    await client.post(
        "/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "B", "price": 5, "quantity": 4}
    )

    response = await client.get(
        "/inventory/value",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

 
    assert response.json()["total_value"] == 40



#--
@pytest.mark.asyncio
async def test_update_product_zero_quantity_bug(client, admin_token):
    create = await client.post(
        "/products",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"name": "Test", "price": 100, "quantity": 10}
    )

    product_id = create.json()["id"]

    update = await client.put(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"quantity": 0}
    )


    assert update.json()["quantity"] == 0


#--
@pytest.mark.asyncio
async def test_delete_nonexistent_product(client, admin_token):
    response = await client.delete(
        "/products/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 204
