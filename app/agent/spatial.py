"""
SAM 3.1 Spatial Segmentation Agent for Kasi-Logistics
Clusters unstructured township delivery coordinates into micro-zones and routing corridors.
"""
from typing import List, Dict, Any
import math

class SpatialSegmentationAgent:
    def __init__(self, cluster_radius_km: float = 1.5):
        self.cluster_radius_km = cluster_radius_km

    def segment_delivery_nodes(self, stops: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Segments a list of delivery stops into spatial clusters/corridors
        simulating SAM 3.1 spatial coordinate partitioning.
        """
        if not stops:
            return {"zones": [], "total_clusters": 0}

        unprocessed = list(stops)
        clusters = []

        while unprocessed:
            current = unprocessed.pop(0)
            current_lat, current_lon = current["coordinates"]
            zone_stops = [current]
            
            remaining = []
            for stop in unprocessed:
                lat, lon = stop["coordinates"]
                distance = self._haversine_distance(current_lat, current_lon, lat, lon)
                
                if distance <= self.cluster_radius_km:
                    zone_stops.append(stop)
                else:
                    remaining.append(stop)
            
            unprocessed = remaining
            clusters.append({
                "zone_id": f"zone_{len(clusters) + 1}",
                "stop_count": len(zone_stops),
                "total_volume_kg": sum(s.get("order_volume_kg", 0.0) for s in zone_stops),
                "stops": zone_stops
            })

        return {
            "algorithm": "SAM-3.1-Spatial-Segmentation",
            "total_clusters": len(clusters),
            "zones": clusters
        }

    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great-circle distance between two GPS coordinates in kilometers."""
        R = 6371.0  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        return R * c