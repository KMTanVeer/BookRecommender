# app.py (final patched version)
from flask import Flask, render_template, request, url_for
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)

def load_pickle(name):
    path = os.path.join(BASE_DIR, name)
    with open(path, 'rb') as f:
        return pickle.load(f)

def ensure_https(url):
    """Convert url to https if possible and handle protocol-relative urls."""
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if url.startswith('//'):
        return 'https:' + url
    if url.startswith('http://'):
        return url.replace('http://', 'https://', 1)
    return url

# Load pickles once at startup
popular_df = load_pickle('popular.pkl')
pt = load_pickle('pt.pkl')
books = load_pickle('books.pkl')
similarity_scores = load_pickle('similarity_scores.pkl')

app = Flask(__name__)

@app.route('/')
def index():
    # ensure images use https and fallback to placeholder if missing
    images = []
    for u in list(popular_df['Image-URL-M'].values):
        iu = ensure_https(u)
        images.append(iu or url_for('static', filename='placeholder.png'))
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=images,
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = (request.form.get('user_input') or '').strip()
    if not user_input:
        # no input — render same page with no results
        print("Empty user_input received.")
        return render_template('recommend.html', data=[])

    # Try exact match first
    idxs = np.where(pt.index == user_input)[0]
    chosen_index = None

    if idxs.size > 0:
        chosen_index = idxs[0]
    else:
        # Try case-insensitive exact match
        lowered = user_input.lower()
        matches = [i for i, t in enumerate(pt.index) if isinstance(t, str) and t.lower() == lowered]
        if matches:
            chosen_index = matches[0]
        else:
            # Try a "contains" match as last resort (first match)
            contains = [i for i, t in enumerate(pt.index) if isinstance(t, str) and lowered in t.lower()]
            if contains:
                chosen_index = contains[0]

    if chosen_index is None:
        # Not found — return no results (don't crash)
        print(f"User input not found in pt.index: '{user_input}'")
        return render_template('recommend.html', data=[])

    # compute similar items (skip the item itself and take top 4)
    similar_items = sorted(list(enumerate(similarity_scores[chosen_index])),
                           key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        # i[0] is the index of the similar book in pt.index
        book_title = pt.index[i[0]]
        temp_df = books[books['Book-Title'] == book_title]

        # get unique entry for that title
        unique = temp_df.drop_duplicates('Book-Title')

        # safe extraction: if values exist, grab them, otherwise fallback
        title_vals = list(unique['Book-Title'].values) if 'Book-Title' in unique.columns else []
        author_vals = list(unique['Book-Author'].values) if 'Book-Author' in unique.columns else []
        # try 'Image-URL-M' or 'Image-URL-L' or 'Image-URL-S'
        image_vals = []
        for col in ('Image-URL-M', 'Image-URL-L', 'Image-URL-S', 'image', 'img', 'cover'):
            if col in unique.columns:
                image_vals = list(unique[col].values)
                if image_vals:
                    break

        title = title_vals[0] if len(title_vals) > 0 else 'Unknown title'
        author = author_vals[0] if len(author_vals) > 0 else 'Unknown author'
        image = image_vals[0] if len(image_vals) > 0 else None

        # ensure https for image; fallback to static placeholder if necessary
        image = ensure_https(image) or url_for('static', filename='placeholder.png')

        data.append([title, author, image])

    print("Recommendations:", data)
    return render_template('recommend.html', data=data)


# ---------------- Contact Page ----------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Capture form input
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        message = (request.form.get('message') or '').strip()

        # Print to console (shows in Render logs too)
        print("📩 New Contact Message:", {"name": name, "email": email, "message": message})

        # Show success message
        return render_template('contact.html', success=True, name=name)

    # On GET request → just show page
    return render_template('contact.html', success=False)


if __name__ == '__main__':
    app.run(debug=True)
