import pytest
from rest_framework.test import APIClient

from .models import Product, ProductOption, Tag

# 현재 파일의 모든 테스트코드에 DB 접근 가능 mark 부여
pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def product_data():
    """CRUD 테스트 중 DB에 Product 데이터가 필요한 경우 사용한다."""
    product = Product.objects.create(name="TestProduct")

    ProductOption.objects.create(product=product, name="TestOption1", price="1000")
    ProductOption.objects.create(product=product, name="TestOption2", price="500")
    ProductOption.objects.create(product=product, name="TestOption3", price="0")

    tag1 = Tag.objects.create(name="ExistTag")
    tag2 = Tag.objects.create(name="NewTag")
    product.tag_set.add(tag1, tag2)

    Product.objects.create(name="TestProduct2")

    return product


def test_create(api_client):
    # 기존에 존재하는 태그 하나 미리 생성
    Tag.objects.create(name="ExistTag")

    response = api_client.post(
        "/shop/products/",
        {
            "name": "TestProduct",
            "option_set": [
                {"name": "TestOption1", "price": 1000},
                {"name": "TestOption2", "price": 500},
                {"name": "TestOption3", "price": 0}
            ],
            "tag_set": [
                {"pk": 1, "name": "ExistTag"},
                {"name": "NewTag"}
            ]
        },
        format="json"
    )

    assert response.status_code == 201

    assert Product.objects.filter(name="TestProduct").exists()

    product = Product.objects.get(pk=1)
    assert product.option_set.count() == 3

    tag_name = list(product.tag_set.values_list("name", flat=True))
    assert "ExistTag" in tag_name
    assert "NewTag" in tag_name
    assert len(tag_name) == 2


def test_update(api_client, product_data):
    response = api_client.patch(
        f"/shop/products/{product_data.pk}/",
        {
            "pk": 1,
            "name": "TestProduct",
            "option_set": [
                {
                    "pk": 1,
                    "name": "TestOption1",
                    "price": 1000
                },
                {
                    "pk": 2,
                    "name": "Edit TestOption2",
                    "price": 1500
                },
                {
                    "name": "Edit New Option",
                    "price": 300
                }
            ],
            "tag_set": [
                {"pk": 1, "name": "ExistTag"},
                {"pk": 2, "name": "NewTag"},
                {"name": "Edit New Tag"}
            ]
        },
        format="json"
    )

    assert response.status_code == 200

    product_data.refresh_from_db()
    edit_opt = product_data.option_set.get(pk=2)
    assert edit_opt.name == "Edit TestOption2"
    assert edit_opt.price == 1500
    assert product_data.option_set.filter(name="Edit New Option").exists()

    assert product_data.tag_set.filter(name="Edit New Tag").exists()
    assert Tag.objects.count() == 3


def test_list(api_client, product_data):
    response = api_client.get("/shop/products/")

    assert response.status_code == 200

    assert len(response.data) == Product.objects.count()


def test_retrieve(api_client, product_data):
    response = api_client.get(f"/shop/products/{product_data.pk}/")

    assert response.status_code == 200

    assert response.data["name"] == product_data.name


def test_delete(api_client, product_data):
    response = api_client.delete(f"/shop/products/{product_data.pk}/")

    assert response.status_code == 204

    assert not Product.objects.filter(pk=product_data.pk).exists()
