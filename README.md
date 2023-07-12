## FGT Purchase Order/Agreement Project 

### Python/Flask with PostgreSQL database

Project structure:
```
.
├── compose.yaml
└── flask
    ├── Dockerfile
    ├── requirements.txt
    └── server.py

```

[_compose.yaml_](compose.yaml)
```
services:
  flask_app:
    build: .
    ...
  flask_db:
    image: postgres:12
    ...
```
The compose file defines an application with two services `backend` and `db`.
When deploying the application, docker compose maps port 4000 of the proxy service container to port 4000 of the host as specified in the file.
Make sure port 4000 on the host is not already being in use.

## Deploy with docker compose

```
$ docker compose up -d
Building 1.0s (11/11) FINISHED
...
...
WARNING: Image for service proxy was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
 ✔ Network fgt-project_default  Created
 ✔ Container flask_db           Started
 ✔ Container flask_app          Started
```

## Expected result

Listing containers should show three containers running and the port mapping as below:
```
$ docker compose ps
NAME                IMAGE                                  COMMAND                  SERVICE             CREATED             STATUS              PORTS
flask_app           andreasmodsquad/flask_live_app:1.0.0   "flask run --host=0.…"   flask_app           3 minutes ago       Up 3 minutes        0.0.0.0:4000->4000/tcp
flask_db            postgres:12                            "docker-entrypoint.s…"   flask_db            3 minutes ago       Up 3 minutes        0.0.0.0:5432->5432/tcp
```

After the application starts, navigate to `http://localhost:4000` in your web browser or run:
```
$ curl localhost:4000
{ "message": "hello world" }
```

Stop and remove the containers
```
$ docker compose down
```

## Project Planning

### 1. Endpoints

POST /purchase_agreement
- params: { total_quantity: int, end_date: date, vendor_id: uuid }
- return success

POST /purchase_order
- params: { quantity: int, plant_type_id: uuid, vendor_id: uuid }
- return success
- errors:
  - if purchase order too big

PUT /purchase_order/<int:id>
- params: { purchase_order_id: uuid }
- logic: update purchase_order received & create new plants
- return success

(Seed endpoints)
POST /vendor
- params: { name: string }
POST /plant_type
- params: { name: string }

### 2. Data Model

Vendor
- id: bigint
- name: String

PurchaseAgreement
- id: bigint
- total_quantity: int
- end_date: DateTime
- updated_at: DateTime
- created_at: DateTime
- vendor_id: bigint
- purchase_orders_quantity_total: int (Denormalized)
- is_complete: boolean (Denormalized = Date.now() > end_date OR purchase_orders_quantity_total == total_quantity)

PurchaseOrder
- id: bigint
- quantity: int
- is_received: boolean
- updated_at: DateTime
- created_at: DateTime
- plant_type_id: int
- vendor_id: bigint
- purchase_agreement_id: bigint (Optional) 

PlantType
- id: int
- name: String

Plant
- id: bigint
- created_at: DateTime
- plant_type_id: int

### 3. Assumptions for Simplicity:
- We don't need to keep track of the specific plants on POs (Plants are plants once they reach our Inventory)
- There is no User model and no access control. This is accessible only by admins.
- We will seed the Vendors and PlantTypes rather than allowing creation.
- 1(Vendor) to many (PA) relationship
- 1(Vendor) to many (PO) relationship