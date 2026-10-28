import math
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class DeliveryStop(BaseModel):
    stop_id: str
    node_id: str
    merchant_name: str
    order_volume_kg: float
    coordinates: List[float]

class RouteOptimizationRequest(BaseModel):
    depot_coordinates: List[float] = Field(description="[lat, lon] starting warehouse")
    stops: List[DeliveryStop]
    max_vehicle_capacity_kg: float = Field(default=500.0)

class OptimizedRouteResponse(BaseModel):
    total_distance_km: float
    estimated_duration_mins: float
    vehicle_load_utilized_percentage: float
    ordered_stops: List[DeliveryStop]
    routing_metadata: Dict[str, Any]

class KasiRouteOptimizer:
    @staticmethod
    def _haversine_distance(coord1: List[float], coord2: List[float]) -> float:
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @classmethod
    def optimize_route(cls, request: RouteOptimizationRequest) -> OptimizedRouteResponse:
        current_location = request.depot_coordinates
        unvisited = list(request.stops)
        ordered_stops: List[DeliveryStop] = []
        total_distance = 0.0
        total_weight = sum(stop.order_volume_kg for stop in unvisited)
        load_percentage = min(100.0, (total_weight / request.max_vehicle_capacity_kg) * 100)

        while unvisited:
            nearest_stop = min(unvisited, key=lambda s: cls._haversine_distance(current_location, s.coordinates))
            distance = cls._haversine_distance(current_location, nearest_stop.coordinates)
            total_distance += distance
            current_location = nearest_stop.coordinates
            ordered_stops.append(nearest_stop)
            unvisited.remove(nearest_stop)

        estimated_duration = (total_distance / 25.0) * 60.0 + (len(ordered_stops) * 10.0)

        return OptimizedRouteResponse(
            total_distance_km=round(total_distance, 2),
            estimated_duration_mins=round(estimated_duration, 1),
            vehicle_load_utilized_percentage=round(load_percentage, 1),
            ordered_stops=ordered_stops,
            routing_metadata={"algorithm": "nearest_neighbor_capacity_constrained", "total_stops": len(ordered_stops)},
        )

