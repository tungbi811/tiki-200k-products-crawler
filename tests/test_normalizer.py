from etl.transform.normalizer import (
    normalize_description,
    normalize_product
)

def test_normalize_description_remove_html():
    text = "<p>Hello <b>world</b></p>"
    result = normalize_description(text)
    assert result == "Hello world"

def test_normalize_description_extra_spaces():
    text = "Hello    world   !"
    result = normalize_description(text)
    assert result == "Hello world !"

def test_normalize_description_empty():
    assert normalize_description(None) == ""
    assert normalize_description("") == ""

def test_normalize_product_basic():
    data = {
        "id": 1,
        "name": "Product A",
        "url_key": "product-a",
        "price": 100,
        "description": "<p>Nice   product</p>",
        "images": [
            {"base_url": "img1.jpg"},
            {"base_url": "img2.jpg"},
        ],
    }

    result = normalize_product(data)

    assert result["id"] == 1
    assert result["name"] == "Product A"
    assert result["url_key"] == "product-a"
    assert result["price"] == 100
    assert result["description"] == "Nice product"
    assert result["images"] == ["img1.jpg", "img2.jpg"]

def test_normalize_product_ignore_invalid_images():
    data = {
        "description": "test",
        "images": [
            {"base_url": "img1.jpg"},
            "bad",
            {},
        ],
    }

    result = normalize_product(data)
    assert result["images"] == ["img1.jpg"]
