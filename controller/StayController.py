from fastapi import APIRouter, Request, Response, HTTPException, Query
from repository import StayRepository
from util import Database, RedisSession
from dtypes import APIResponse, HttpStatus

router = APIRouter(prefix="/api/v1/stays")
stay_service = StayRepository(
    db_session=Database(),
    redis_session=RedisSession()
)


@router.post("/")
async def create_stay(
        request: Request,
        response: Response
):
    body = await request.json()
    host_id = body.get("host_id")
    stay_name = body.get("stay_name")
    description = body.get("description")
    line1 = body.get("line1")
    line2 = body.get("line2")
    city = body.get("city")
    state = body.get("state")
    postal_code = body.get("postal_code")
    country = body.get("country")
    price_per_night = body.get("price_per_night")
    max_guests = body.get("max_guests")
    num_bedrooms = body.get("num_bedrooms")
    area = body.get("area")
    num_bathrooms = body.get("num_bathrooms")
    rules = body.get("rules")
    amenities = body.get("amenities")
    pictures = body.get("pictures")
    lat = body.get("lat")
    long = body.get("long")

    success, err = await stay_service.create_stay(
        host_id, stay_name, description, line1, line2, city, state, postal_code, country, price_per_night, max_guests,
        num_bedrooms, area, num_bathrooms, rules, amenities, pictures, lat, long
    )

    if not success:
        raise HTTPException(status_code=500, detail=err)
    api_response = APIResponse(status=HttpStatus.OK, message="Stay Created", data=None)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/{stay_id}")
async def get_stay(stay_id: str, response: Response):
    result_set = await stay_service.get_stay_by_id(stay_id)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=result_set)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/city/{city}")
async def get_stay_city(
        city: str,
        response: Response,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
):
    result_set = await stay_service.get_stays_by_city(city, limit, offset)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=result_set)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/state/{state}")
async def get_stay_state(
        state: str,
        response: Response,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
):
    result_set = await stay_service.get_stays_by_state(state, limit, offset)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=result_set)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/country/{country}")
async def get_stay_country(
        country: str,
        response: Response,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
):
    result_set = await stay_service.get_stays_by_country(country, limit, offset)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=result_set)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/zip/{postal_code}")
async def get_stay_postal_code(
        postal_code: str,
        response: Response,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
):
    result_set = await stay_service.get_stays_by_postal_code(postal_code, limit, offset)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=result_set)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.get("/host/{host_id}")
async def get_stay_host(
        host_id: str,
        response: Response,
        limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0)
):
    result_set = await stay_service.get_stays_by_host(host_id, limit, offset)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=result_set)
    response.status_code = api_response.status.value
    return api_response.to_dict()


@router.post("/{stay_id}/book")
async def mark_booked(stay_id: str, request: Request, response: Response):
    body = await request.json()
    user_id = body.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    success, err = await stay_service.mark_stay_as_booked(stay_id, user_id)
    if not success:
        raise HTTPException(status_code=500, detail=err)
    api_response = APIResponse(status=HttpStatus.OK, message="Fetched Results", data=None)
    response.status_code = api_response.status.value
    return api_response.to_dict()
