import os
import django
import sys
import requests
import time
from django.core.files.base import ContentFile
from duckduckgo_search import DDGS

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.products.models import Product

def get_image_url(query):
    try:
        results = DDGS().images(
            keywords=query + " product india packaging",
            region="in-en",
            safesearch="on",
            max_results=3
        )
        if results:
            return results[0]['image']
    except Exception as e:
        print(f"  [!] DDGS error for '{query}': {e}")
    return None

def download_image_and_save(product, image_url):
    try:
        response = requests.get(image_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            file_ext = image_url.split('?')[0].split('.')[-1]
            if len(file_ext) > 4 or not file_ext:
                file_ext = 'jpg'
                
            file_name = f"{product.slug}_main.{file_ext}"
            
            # Save to product
            product.image_main.save(file_name, ContentFile(response.content), save=True)
            print(f"  [+] Saved {file_name}")
            return True
        else:
            print(f"  [-] Failed to download, status code: {response.status_code}")
    except Exception as e:
        print(f"  [-] Error downloading image: {e}")
    return False

def main():
    products = Product.objects.all()
    total = products.count()
    print(f"Found {total} products to process.")

    for idx, product in enumerate(products, 1):
        if product.image_main:
            print(f"[{idx}/{total}] Skipping '{product.name}' (already has image)")
            continue
            
        print(f"[{idx}/{total}] Processing '{product.name}'...")
        
        # We will try up to 2 times with different queries
        queries = [
            f"{product.name} grocery",
            product.name
        ]
        
        success = False
        for query in queries:
            img_url = get_image_url(query)
            if img_url:
                print(f"  [~] Downloading from {img_url[:60]}...")
                if download_image_and_save(product, img_url):
                    success = True
                    break
            time.sleep(1) # Be nice to DDG
            
        if not success:
            print(f"  [!] Could not get image for '{product.name}'")

if __name__ == '__main__':
    main()
