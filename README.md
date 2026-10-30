# 🌍 Kasi-Logistics & PayMerch AI
### Meta SAM 3.1 Powered Township Logistics & Closed-Loop Fintech Escrow

**Kasi-Logistics & PayMerch** is an enterprise-grade spatial dispatching and closed-loop fintech escrow platform engineered for unmapped informal settlements, wholesale supply chains, and spaza merchant networks across the Western Cape, South Africa.

By pairing **Meta’s Segment Anything Model 3.1 (SAM 3.1)** computer vision framework with real-road OSRM network routing and mobile money escrow, Kasi-Logistics bridges the critical "last-mile gap" in informal markets where formal street maps end.

---

## 👁️ Meta SAM 3.1 Spatial Vision Integration

Informal settlements across Cape Town (Khayelitsha, Gugulethu, Langa) consist of dense, unmapped alleyways inaccessible to standard GPS navigation systems. Kasi-Logistics deploys **Meta SAM 3.1** to solve spatial partitioning and micro-corridor navigation:

* **Zero-Shot Alleyway Segmentation:** Runs SAM 3.1 spatial prompt processing on aerial imagery and ground footage to detect traversable widths, informal paths, and obstacle nodes.
* **Micro-Zone Coordinate Clustering:** Extends SAM 3.1 spatial partitioning logic into coordinate clustering algorithms, grouping unstructured spaza delivery stops into optimized delivery corridors.
* **Geofenced Arrival Verification:** Works alongside spatial vision markers to validate delivery vehicle arrival before releasing locked wholesale escrow funds.

---

## 🏗️ Technical Architecture & System Flow

+-----------------------------------------------------------------------------------+
|                                 Frontend Dashboard                                |
|   (Leaflet.js + OSM Street Map Labels & Landmarks / Esri Satellite Toggle)        |
+------------------------------------------+----------------------------------------+
| REST / CORS Bridge
v
+-----------------------------------------------------------------------------------+
|                            FastAPI Backend Engine (:8092)                         |
+------------------------------------------+----------------------------------------+
|
+---------------------------------+---------------------------------+
|                                 |                                 |
v                                 v                                 v
+------------------+             +-------------------+             +------------------+
|   Meta SAM 3.1   |             |  OSRM Routing &   |             |     PayMerch     |
| Spatial Segmenter|             | Geo-Spatial Agent |             |  Escrow Fintech  |
+--------+---------+             +---------+---------+             +--------+---------+
|                                 |                                 |
v                                 v                                 v
Alleyway Vision Mapping           Real Physical Roads               Netlify Mobile Wallet
& Micro-Zone Partitioning         (N2, R300, Arterials)             (paymerchmobmoney)


### Component Breakdown
1. **Meta SAM 3.1 Spatial Agent (`app/agent/spatial.py`):** Processes image data and unstructured GPS coordinate matrices into bounded micro-zones and traversable corridor segments.
2. **OSRM Routing Engine:** Queries public Open Source Routing Machine APIs to map multi-stop delivery paths onto real Western Cape highway and arterial networks.
3. **PayMerch Escrow Engine (`app/agent/paymerch.py`):** Manages closed-loop wallet balances, escrow locks (`/v1/paymerch/escrow/create`), and QR code payloads integrated with the live Netlify mobile money app (`https://paymerchmobmoney.netlify.app`).
4. **CORS Middleware (`app/main.py`):** Authorizes secure cross-origin requests between the FastAPI backend and Netlify client applications.

---

## 🛠️ Tech Stack & Dependencies

* **Meta AI Stack:** Meta Segment Anything Model (SAM 3.1) spatial vision pipeline
* **Backend Framework:** Python, FastAPI, Pydantic, Uvicorn, Math (Haversine clustering algorithms)
* **Frontend Interface:** HTML5, Tailwind CSS, JavaScript (ES6+), Leaflet.js
* **Mapping & Spatial Data:** OpenStreetMap (OSM) tile layers with street/landmark labels, Esri World Imagery, public OSRM driving APIs
* **Fintech Bridge:** CORSMiddleware connecting FastAPI with `https://paymerchmobmoney.netlify.app`

---

## 📍 Verified Western Cape Real-World Coverage

Every location marker maps directly to real physical infrastructure, retail nodes, and distribution hubs:

* **Khayelitsha:** Site C Terminus, Harare Fresh Produce, Kuyasa Station, Site B, Lookout Hill Commercial Node
* **Gugulethu:** NY1 Unit 1, Gugulethu Square (NY108), Mau Mau General Dealer (NY78), NY6 Community Market
* **Mitchells Plain:** Town Centre Wholesaling Hub, Mandalay Station, Beacon Valley
* **Langa:** Zone 23, Washington Street, Bhunga Avenue Trading Post
* **Wholesale Hubs:** Bellville MegaWholesale, Epping Industria Distribution Hub, Philippi Industrial Park

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Activate Environment
```powershell
git clone [https://github.com/your-username/kasi-logistics.git](https://github.com/your-username/kasi-logistics.git)
cd kasi-logistics
python -m venv .venv
.venv\Scripts\Activate.ps1
2. Install Dependencies & Launch Server
PowerShell
pip install fastapi uvicorn pydantic requests
uvicorn app.main:app --reload --port 8092
3. Open Interactive Dashboard
Main Control Center: http://localhost:8092

Swagger API Documentation: http://localhost:8092/docs