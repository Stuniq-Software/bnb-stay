from dtypes import Stay
from util import Database, RedisSession
from typing import Optional, List


class StayRepository:
    db_session: Database
    redis_session: RedisSession

    def __init__(self, db_session: Database, redis_session: RedisSession):
        self.db_session = db_session
        self.redis_session = redis_session

    async def create_stay(
            self,
            host_id: str,
            stay_name: str,
            description: str,
            line1: str,
            line2: Optional[str],
            city: str,
            state: str,
            postal_code: str,
            country: str,
            price_per_night: float,
            max_guests: int,
            num_bedrooms: int,
            area: float,
            num_bathrooms: int,
            rules: List[str],
            amenities: List[str],
            pictures: List[str],
            lat: float,
            long: float
    ):
        sql_query = """
        INSERT INTO stays (
            host_id, stay_name, description, address, price_per_night, max_guests, num_bedrooms, area, num_bathrooms, rules, amenities, pictures, lat, long
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        address_query = """
        INSERT INTO address (line1, line2, city, state, country, postal_code) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """

        addr_query, err = self.db_session.execute_query(address_query, (line1, line2, city, state, country, postal_code))
        if err:
            return False, err

        address_id = self.db_session.get_cursor().fetchone()[0]
        self.db_session.execute_query(sql_query, (
            host_id, stay_name, description, address_id,  price_per_night, max_guests,
            num_bedrooms, area, num_bathrooms, rules, amenities, pictures, lat, long
        ), auto_commit=True)

        return True, None

    async def update_stay(self, stay_id: str, **kwargs):
        pass

    async def delete_stay(self, stay_id: str):
        query = "DELETE FROM stays CASCADE WHERE id = %s"
        return self.db_session.execute_query(query, (stay_id,), auto_commit=True)

    async def get_stay_by_id(self, stay_id: str):
        query = "SELECT * FROM stays INNER JOIN address ON stays.address = address.id WHERE stays.id = %s"
        success, err = self.db_session.execute_query(query, (stay_id,))
        if err:
            print(f"Error: {err}")
            return []
        rs = self.db_session.get_cursor().fetchone()
        if not rs:
            return {}
        parsed = Stay.from_tuple(rs).to_dict()
        return parsed

    async def get_stays_by_city(self, city: str, limit: int = 100, offset: int = 0):
        query = ("SELECT * FROM stays INNER JOIN address ON stays.address = address.id WHERE address.city LIKE %s ORDER"
                 " BY stays.id OFFSET %s ROWS LIMIT %s")
        success, err = self.db_session.execute_query(query, (city, offset, limit))
        if err:
            print(f"Error: {err}")
            return []
        rs = self.db_session.get_cursor().fetchall()
        if len(rs) == 0:
            return []
        parsed = [Stay.from_tuple(x).to_dict() for x in rs]
        return parsed

    async def get_stays_by_postal_code(self, postal_code: str, limit: int = 100, offset: int = 0):
        query = ("SELECT * FROM stays INNER JOIN address ON stays.address = address.id WHERE address.postal_code = %s "
                 "ORDER BY stays.id OFFSET %s ROWS LIMIT %s")
        success, err = self.db_session.execute_query(query, (postal_code, offset, limit))
        if err:
            print(f"Error: {err}")
            return []
        rs = self.db_session.get_cursor().fetchall()
        if len(rs) == 0:
            return []
        parsed = [Stay.from_tuple(x).to_dict() for x in rs]
        return parsed

    async def get_stays_by_country(self, country: str, limit: int = 100, offset: int = 0):
        query = ("SELECT * FROM stays INNER JOIN address ON stays.address = address.id WHERE address.country LIKE %s "
                 "ORDER BY stays.id OFFSET %s ROWS LIMIT %s")
        success, err = self.db_session.execute_query(query, (country, offset, limit))
        if err:
            print(f"Error: {err}")
            return []
        rs = self.db_session.get_cursor().fetchall()
        if len(rs) == 0:
            return []
        parsed = [Stay.from_tuple(x).to_dict() for x in rs]
        return parsed

    async def get_stays_by_state(self, state: str, limit: int = 100, offset: int = 0):
        query = ("SELECT * FROM stays INNER JOIN address ON stays.address = address.id WHERE address.state = %s ORDER "
                 "BY stays.id OFFSET %s ROWS LIMIT %s")
        success, err = self.db_session.execute_query(query, (state, offset, limit))
        if err:
            print(f"Error: {err}")
            return []
        rs = self.db_session.get_cursor().fetchall()
        if len(rs) == 0:
            return []
        parsed = [Stay.from_tuple(x).to_dict() for x in rs]
        return parsed

    async def get_stays_by_host(self, host_id: str, limit: int = 100, offset: int = 0):
        query = ("SELECT * FROM stays INNER JOIN address ON stays.address = address.id WHERE stays.host_id = %s ORDER "
                 "BY stays.id OFFSET %s ROWS LIMIT %s")
        success, err = self.db_session.execute_query(query, (host_id, offset, limit))
        if err:
            print(f"Error: {err}")
            return []
        rs = self.db_session.get_cursor().fetchall()
        if len(rs) == 0:
            return []
        parsed = [Stay.from_tuple(x).to_dict() for x in rs]
        return parsed

    async def mark_stay_as_booked(self, stay_id: str, user_id: str):
        query = "UPDATE stays SET booked_by = %s, is_available = false WHERE id = %s"
        success, err = self.db_session.execute_query(query, (user_id, stay_id), auto_commit=True)
        if err:
            print(f'Error: {err}')
            return False
        return True

    async def mark_stay_as_unbooked(self, stay_id: str):
        query = "UPDATE stays SET booked_by = null, is_available = true WHERE id = %s"
        success, err = self.db_session.execute_query(query, (stay_id,), auto_commit=True)
        if err:
            print(f'Error: {err}')
            return False
        return True
