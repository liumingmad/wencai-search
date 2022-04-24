docker build -t wcs .

docker run -dit -p 9901:8080 52f server.py

# docker exec -it cefd bash

python3 -m http.server 7800