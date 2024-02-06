CREATE TABLE IF NOT EXISTS stays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    host_id UUID REFERENCES users(id),
    stay_name TEXT NOT NULL,
    description TEXT NOT NULL,
    address UUID REFERENCES address(id),
    price_per_night DECIMAL NOT NULL,
    max_guests INT NOT NULL,
    num_bedrooms INT NOT NULL,
    area DECIMAL NOT NULL,
    num_bathrooms INT NOT NULL,
    rules TEXT[20] NOT NULL,
    amenities TEXT[30] NOT NULL,
    pictures TEXT[10] NOT NULL,
    lat DECIMAL NOT NULL,
    long DECIMAL NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    booked_by UUID REFERENCES users(id),
    booked_until DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)