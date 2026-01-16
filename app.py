from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            print("[INFO] Form submission received.")
            searchString = request.form['content'].replace(" ", "")
            print(f"[DEBUG] Search string cleaned: {searchString}")

            flipkart_url = f"https://www.flipkart.com/search?q={searchString}"
            print(f"[DEBUG] Flipkart URL: {flipkart_url}")

            # 1️⃣ Fetch search results with headers
            headers = {"User-Agent": "Mozilla/5.0"}
            search_resp = requests.get(flipkart_url, headers=headers, timeout=10)
            search_resp.encoding = 'utf-8'
            flipkart_html = bs(search_resp.text, "html.parser")
            print("[INFO] Flipkart search page fetched.")

            # 2️⃣ Grab all product anchors
            product_anchors = flipkart_html.find_all("a", class_="CGtC98")
            print(f"[DEBUG] Found {len(product_anchors)} product anchors")

            if not product_anchors:
                return "No products found – Flipkart’s layout may have changed."

            # 3️⃣ Build the first product link
            first_href = product_anchors[0].get("href")
            productLink = "https://www.flipkart.com" + first_href
            print(f"[DEBUG] Product link: {productLink}")

            # 4️⃣ Fetch the product page
            prodRes = requests.get(productLink, headers=headers, timeout=10)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print("[INFO] Product page fetched and parsed.")

            # 5️⃣ Scrape reviews
            commentboxes = prod_html.find_all('div', class_="_16PBlm")
            print(f"[DEBUG] Number of comment boxes: {len(commentboxes)}")

            filename = f"{searchString}.csv"
            with open(filename, "w", encoding="utf-8") as fw:
                fw.write("Product,Customer Name,Rating,Heading,Comment\n")

                reviews = []
                for i, commentbox in enumerate(commentboxes):
                    print(f"[INFO] Processing comment box #{i+1}")
                    # Name
                    try:
                        name = commentbox.find('p', class_='_2sc7ZR _2V5EHH').text
                    except:
                        name = 'No Name'
                    # Rating
                    try:
                        rating = commentbox.div.div.div.div.text
                    except:
                        rating = 'No Rating'
                    # Heading
                    try:
                        commentHead = commentbox.div.div.div.p.text
                    except:
                        commentHead = 'No Comment Heading'
                    # Comment
                    try:
                        custComment = commentbox.find_all('div', class_='')[0].div.text
                    except:
                        custComment = 'No Comment'

                    reviews.append({
                        "Product": searchString,
                        "Name": name,
                        "Rating": rating,
                        "CommentHead": commentHead,
                        "Comment": custComment
                    })
                    fw.write(f"{searchString},{name},{rating},{commentHead},{custComment}\n")

            print("[INFO] All reviews written to CSV successfully.")
            # Pass reviews (dropping the last empty entry if any) into results.html
            return render_template('result.html', reviews=reviews[:-1] or reviews)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"An error occurred: {e}"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
