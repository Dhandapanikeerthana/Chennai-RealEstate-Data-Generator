import pandas as pd
import numpy as np

np.random.seed(42)

localities_data = {
    'Anna Nagar': {'base_price':14500000, 'avg_int_sqft':1800, 'sqft_variance':200},
    'Velacherry': {'base_price':7500000, 'avg_int_sqft':1200, 'sqft_variance':150},
    'Tambaram': {'base_price':4200000, 'avg_int_sqft':900, 'sqft_variance':100},
    'T Nagar': {'base_price':13000000, 'avg_int_sqft':1600, 'sqft_variance':180},
    'Porur': {'base_price':6200000, 'avg_int_sqft':1100, 'sqft_variance':130},
    'OMR': {'base_price':8800000, 'avg_int_sqft':1400, 'sqft_variance':160},
    'Avadi': {'base_price':3200000, 'avg_int_sqft':800, 'sqft_variance':90},
    'Adyar': {'base_price':13800000, 'avg_int_sqft':1700, 'sqft_variance':190},
    'Perambur': {'base_price':4500000, 'avg_int_sqft':950, 'sqft_variance':110},
    'Chromepet': {'base_price':5600000, 'avg_int_sqft':1050, 'sqft_variance':120},
    'Mylapore': {'base_price':12000000, 'avg_int_sqft':1500, 'sqft_variance':170},
    'Nungambakkam': {'base_price':11500000, 'avg_int_sqft':1400, 'sqft_variance':180},
    'Guindy': {'base_price':9500000, 'avg_int_sqft':1300, 'sqft_variance':150},
    'Egmore': {'base_price':8200000, 'avg_int_sqft':1250, 'sqft_variance':145},
    'Chetpet': {'base_price':10800000, 'avg_int_sqft':1450, 'sqft_variance':165},
    'Kodambakkam': {'base_price':7800000, 'avg_int_sqft':1150, 'sqft_variance':135},
    'Thiruvanmiyur': {'base_price':9200000, 'avg_int_sqft':1280, 'sqft_variance':130},
    'Besant Nagar': {'base_price':10500000, 'avg_int_sqft':1350, 'sqft_variance':120},
    'Saidapet': {'base_price':6800000, 'avg_int_sqft':1100, 'sqft_variance':130},
}

sale_conditions = ["Normal Sale", "Partial", "Abnormal", "Family"]
sale_condition_weights = [0.70, 0.15, 0.10, 0.05]


def generate_bedroom_bathroom(int_sqft):
    if int_sqft < 1000:
        return np.random.choice([1,2]), np.random.choice([1,2])
    elif int_sqft < 1400:
        return np.random.choice([2,3]), np.random.choice([1,2])
    else:
        return np.random.choice([3,4]), np.random.choice([2,3,4])


def generate_n_room(n_bedroom, n_bathroom):
    return n_bedroom + n_bathroom + 2 + np.random.choice([0,1])


def calculate_price(locality, int_sqft, n_bedroom, dist_mainroad, sale_condition, park_facil):

    base_price = localities_data[locality]['base_price']
    avg_sqft = localities_data[locality]['avg_int_sqft']

    size_factor = int_sqft / avg_sqft
    distance_impact = max(0.85, 1 - (dist_mainroad / 1000) * 0.1)
    bedroom_multiplier = 1 + (n_bedroom - 2) * 0.08

    sale_condition_multiplier = {
        'Normal Sale': 1.00,
        'Partial': 0.92,
        'Abnormal': 0.85,
        'Family': 0.88,
    }

    parking_multiplier = 1.05 if park_facil == "Yes" else 1.0

    price = (
        base_price *
        size_factor *
        distance_impact *
        bedroom_multiplier *
        sale_condition_multiplier[sale_condition] *
        parking_multiplier
    )

    variance = np.random.uniform(0.92, 1.08)
    price *= variance

    return int(round(price / 100000) * 100000)


print("Generating Chennai data...")

n_records = 50000
data = []
localities_list = list(localities_data.keys())

for i in range(n_records):
    area = np.random.choice(localities_list)
    int_sqft = max(500, int(np.random.normal(
        localities_data[area]['avg_int_sqft'],
        localities_data[area]['sqft_variance']
    )))

    dist_mainroad = min(int(np.random.exponential(250)), 1000)
    sale_condition = np.random.choice(sale_conditions, p=sale_condition_weights)
    parking_facil = np.random.choice(["Yes", "NO"], p=[0.8, 0.2])

    n_bedroom, n_bathroom = generate_bedroom_bathroom(int_sqft)
    price = calculate_price(area, int_sqft, n_bedroom, dist_mainroad, sale_condition, parking_facil)

    data.append({
        'AREA': area,
        'INT_SQFT': int_sqft,
        'DIST_MAINROAD': dist_mainroad,
        'N_BEDROOM': n_bedroom,
        'N_BATHROOM': n_bathroom,
        'SALE_COND': sale_condition,
        'PARKING_FACIL': parking_facil,
        'PRICE': price
    })

    if (i + 1) % 10000 == 0:
        print(f"Generated {i+1} records...")

df = pd.DataFrame(data)
df.to_csv("chennai_real_estate_50k.csv", index=False)

print("Dataset created successfully!")
print(f"Total records: {len(df):,}")
print(df.head())
