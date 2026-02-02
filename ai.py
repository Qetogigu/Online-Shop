{% extends 'base.html' %}
{% block content %}

<h2>Ask AI for Product Recommendations</h2>

<form method="POST">
    <textarea name="question" class="form-control"
              placeholder="What are you looking for?"></textarea>

    <input type="number" name="min_price" placeholder="Min Price">
    <input type="number" name="max_price" placeholder="Max Price">

    <button class="btn btn-success mt-2">
        Find Best Products
    </button>
</form>

{% if recommendations %}
<h3>AI Recommended Products</h3>

<ul class="list-group">
    {% for product in recommendations %}
    <li class="list-group-item">
        <a href="{{ url_for('product_detail', product_id=product.id) }}">
            {{ product.name }} - ${{ product.price }}
        </a>
    </li>
    {% endfor %}
</ul>
{% endif %}


{% endblock %}
