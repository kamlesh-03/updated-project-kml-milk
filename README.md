# KML Milk Pvt Ltd — Python Django Dairy Commerce + Kubernetes CI/CD

Farm-first dairy e-commerce platform for **KML Milk Pvt Ltd / KML Agros**.

Company:
- KML Agros, Pimpalgaon Khambi, Ta. Arjuni Morgaon, Dist. Gondia, Maharashtra 441702
- Phone / WhatsApp: +91 9923573738
- Brand: Dudhbar by KML Agro Farms

## Features

- Dedicated clickable pages instead of a single long-scroll shop.
- Sections:
  1. Butter, Ghee & Cheese — configurable 100g–950g packs.
  2. Fresh Milk & Curd — configurable 200ml–960ml packs.
  3. Dudhbar ice cream — designed for nearby dairy/grocery retail distribution.
- Admin-managed prices, stock, pack sizes, shelf life/expiry estimate, images, ingredients, usage and farm diary.
- English / Marathi / Hindi language selector.
- Customer registration and login with username, email or phone + password.
- Customer address.
- Website order form.
- One-click WhatsApp order.
- Django Admin for operational control.
- `/health/` Kubernetes health endpoint.
- Docker + Jenkins + Kubernetes.
- Kubernetes `LoadBalancer` service; on Minikube use `minikube tunnel`.

## 1. Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations accounts shop
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 2. Add products

In Admin create categories and products. Example pack values:
- Butter/Ghee/Cheese: 100, 200, 500, 750, 900, 950 g
- Milk/Curd: 200, 500, 750, 900, 960 ml

**Prices are intentionally admin-controlled**, so current market rates can be updated without changing code.

For every product, set `expiry_days`. The product page calculates an expected expiry date from the current date. For a real packaged-food operation, the actual printed batch expiry should remain the legal source of truth.

## 3. Docker

```bash
docker build -t kamlesh-03/kml-milk:latest .
docker run --rm -p 8000:8000 \
  -e DJANGO_DEBUG=False \
  -e DJANGO_SECRET_KEY='replace-this' \
  kamlesh-03/kml-milk:latest
```

## 4. GitHub

```bash
git init
git add .
git commit -m "Initial KML Milk Django dairy platform"
git branch -M main
git remote add origin https://github.com/kamlesh-03/kml-milk-dairy.git
git push -u origin main
```

Change the repository URL if your GitHub repository name is different.

## 5. Docker Hub

The Jenkinsfile expects the Docker image name:

```text
DOCKERHUB_USERNAME/kml-milk
```

In Jenkins, change `DOCKERHUB_USERNAME` to your Docker Hub username.

## 6. Minikube

```bash
minikube start --driver=docker
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl -n kml-milk get pods
minikube tunnel
```

Then in another terminal:

```bash
kubectl -n kml-milk get svc
```

The service is `LoadBalancer`.

## 7. Jenkins

Required Jenkins credentials:
- `dockerhub-creds` → Docker Hub username/password or access token.
- Jenkins agent must have Docker CLI and kubectl.
- For Minikube on the same machine, Jenkins must be able to reach the Kubernetes cluster.

Pipeline stages:
1. Checkout
2. Python Test
3. Docker Build
4. Docker Push
5. Kubernetes Deploy
6. Rollout verification

## Production next steps

For a real nationwide dairy business, add:
- PostgreSQL + persistent backups
- Redis/Celery for order notifications
- payment gateway
- delivery zones and pincode serviceability
- batch/lot tracking
- actual batch expiry fields
- invoice/GST workflow
- inventory reservations
- cold-chain logistics
- rate history rather than silently changing historical order prices
- object storage/CDN for product images
- HTTPS/TLS and domain
- centralized logs and monitoring
- role-based admin permissions
