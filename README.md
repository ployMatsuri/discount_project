# Full Name
**Vimonsiri Thammada**

# Discount Module Assignment

This project provides a discount calculator that can apply various types of discounts to a list of items in a shopping cart. It supports different discount categories such as Coupon (fixed and percentage), On Top (category-based or point-based), and Seasonal (discount applied for every specific amount spent).

## Features
- **Coupon Discounts**: Apply fixed or percentage-based discounts to the entire cart.
- **On Top Discounts**: Apply discounts to specific categories or based on points.
- **Seasonal Discounts**: Apply discounts every time the total spending reaches a certain threshold.
- **Web Interface**: Upload JSON files to calculate discounts via a simple web interface.

  ## Requirements
- Python 3.x
- Docker (for containerization)

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/ployMatsuri/discount_project.git
cd discount_project
```

### 2. Install dependencies (optional if you're not using Docker):
```bash
pip install -r requirements.txt
```

## Using Docker

To run this project using Docker, follow these steps:

### 1. Build the Docker image:
Make sure you are in the project directory where the `Dockerfile` is located. Build the Docker image with the following command:

```bash
docker build -t discount-app .
```

### 2. Run the Docker container:
After building the image, run the container with the following command:

```bash
docker run -p 5000:5000 discount-app
```

This will start the application on port 5000.

### 3. Access the web interface:
Open your browser and go to `http://localhost:5000`. You can upload a JSON file to calculate discounts.

## Usage

1. **Upload a JSON file** containing the items and campaigns for discount calculation.
2. The JSON file should follow the format below:

```json
{
  "items": [
    {"name": "T-Shirt", "price": 350, "category": "Clothing"},
    {"name": "Hat", "price": 250, "category": "Accessories"},
    {"name": "Belt", "price": 230, "category": "Accessories"}
  ],
  "campaigns": [
    {"category": "Coupon", "type": "Fixed", "amount": 50},
    {"category": "On Top", "type": "Point", "points": 68},
    {"category": "Seasonal", "type": "Seasonal", "every": 300, "discount": 40}
  ]
}

or use file **sample_input_pass.json** / **sample_input_fail.json**
```

3. The result will be displayed showing the final price and the details of applied discounts.  
