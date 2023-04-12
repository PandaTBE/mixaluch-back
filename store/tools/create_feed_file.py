from django.http import HttpResponse
import xml.etree.ElementTree as ET

from store.models import ProductImage

from config import HOST_URL, FRONT_PROTOCOL, FRONT_DOMAIN


def create_yml_file(categories, products):
    # create the root element
    yml_catalog = ET.Element('yml_catalog')

    # create the shop element
    shop = ET.SubElement(yml_catalog, 'shop')

    ET.SubElement(shop, 'name').text = "У Михалыча"
    ET.SubElement(shop, 'company').text = "У Михалыча"
    ET.SubElement(shop, 'url').text = f"{FRONT_PROTOCOL}://{FRONT_DOMAIN}"

    currencies = ET.SubElement(shop, 'currencies')

    ET.SubElement(currencies, 'currency', {'id': "RUB", 'rate': "1"})

    # create the categories element
    categories_elem = ET.SubElement(shop, 'categories')
    for category in categories:
        # create the category element with id and text
        ET.SubElement(
            categories_elem, 'category', {
                'id': str(category['id']),
                'parentId': str(category.get('parent_id', ''))
            }).text = category['name']

    # create the offers element
    offers = ET.SubElement(shop, 'offers')
    for product in products:
        images = ProductImage.objects.filter(product_id=product['id']).values()
        main_image = images[0].get('image', '')
        for image in images:
            if image.get('is_feature', False):
                main_image = image.get('image', '')
                break
        # create the offer element with id
        offer = ET.SubElement(offers, 'offer', {'id': str(product['id'])})

        # create the child elements for the offer
        ET.SubElement(offer, 'name').text = product['title']
        ET.SubElement(offer, 'price').text = str(product['regular_price'])
        ET.SubElement(offer, 'currencyId').text = "RUB"
        ET.SubElement(offer, 'categoryId').text = str(product['category_id'])
        ET.SubElement(offer, 'picture').text = f"{HOST_URL}/media/{main_image}"
        ET.SubElement(offer, 'description').text = product['description']
        ET.SubElement(offer,
                      'shortDescription').text = product['description'][:255]

    # create the YML file
    tree = ET.ElementTree(yml_catalog)
    xml_string = ET.tostring(tree.getroot(), encoding='utf-8')
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="feed.xml"'
    response.write(xml_string.decode())
    return response
