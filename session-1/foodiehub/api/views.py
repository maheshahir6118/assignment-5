from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# ==============================================================================
# COLLEGE ASSIGNMENT: JSON vs XML COMPARISON
# ==============================================================================
# Below is a conceptual comparison between JSON and XML representation of data, 
# illustrated using a Flipkart Product example (containing name and price).
#
# 1. JSON (JavaScript Object Notation):
#    - Syntax: Represents data in key-value pairs using curly braces {} and arrays [].
#    - Readability: Extremely lightweight, clean, and highly readable.
#    - Parsing: Native to JavaScript and easily parsed by modern programming languages.
#    - Payload Size: Small, making it fast and efficient for web applications/APIs.
#
#    Flipkart Product Example in JSON:
#    {
#        "name": "Sony WH-1000XM4 Wireless Headphones",
#        "price": 19990.00
#    }
#
# 2. XML (eXtensible Markup Language):
#    - Syntax: Represents data in a hierarchical tree structure using custom tags (<tag>...</tag>).
#    - Readability: More verbose and cluttered compared to JSON due to closing tags.
#    - Parsing: Requires complex parser APIs (like DOM or SAX) to read.
#    - Payload Size: Larger due to repetitive tag markup, consuming more bandwidth.
#
#    Flipkart Product Example in XML:
#    <Product>
#        <Name>Sony WH-1000XM4 Wireless Headphones</Name>
#        <Price>19990.00</Price>
#    </Product>
# ==============================================================================

@api_view(['GET'])
def hello_spotify(request):
    """
    A simple function-based API view using Django REST Framework.
    Returns a JSON response with a greeting message for Spotify fans.
    """
    return Response({
        "message": "Hello, Spotify Fans!"
    })
