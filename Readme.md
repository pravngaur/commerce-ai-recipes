# AI-Driven Product Descriptions

This project demonstrates the capabilities of generating **relevant product descriptions** and **customer review summaries** using AI. It is designed to showcase how e-commerce applications can dynamically generate content tailored to customer personas, intents, and preferences.

**Note**: This application does not provide 1:1 personalization. Instead, it focuses on making the product descriptions and reviews **relevant** based on a broader understanding of customer personas, their tone, priorities, and intent.

In a real-world scenario, the data (e.g., personas, product details, and reviews) would come in real-time from your e-commerce application or data stores. This project uses static data for demonstration purposes.

---

## Features

- Generate **relevant product descriptions** based on customer personas.
- Summarize **relevant customer reviews** tailored to the persona's tone and intent.
- Support for **dynamic personas** with tone, priorities, intent, and confidence levels.
- Easily configurable for different locales and prompt influences.

---

## Project Structure

```
AI_Prod_Descriptions/
├── static/
│   ├── images/
│   │   └── table_jpg.jpg       # Example product image
│   └── ...                     # Other static assets (CSS, JS, etc.)
├── templates/
│   ├── index.html              # Main HTML template for product details
│   └── ...                     # Other HTML templates
├── main.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```


---

## How It Works

1. **Input Data**:
   - The application uses personas (e.g., family, student, professional) and product details (e.g., name, price, description, reviews) as input.
   - The `personas.json` file defines the tone, priorities, intent, and confidence for each persona.

2. **AI-Powered Content Generation**:
   - The `model_call.py` file generates prompts for AI models to create personalized product descriptions and review summaries.
   - The AI model tailors the output based on the persona's tone, intent, and confidence.

3. **Frontend**:
   - The `index.html` template displays the product details, personalized descriptions, and review summaries dynamically. This page exists for demo purpose, in your projects you would take the JSON response and inject in your own frontend.

---

## Features

- **Product Details**: Displays product name, price, and description.
- **Persona Selection**: Allows users to select a persona to tailor the experience.
- **Customer Insights**: AI-refined summaries of customer reviews.
- **Responsive Design**: Ensures compatibility across devices.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI_Prod_Descriptions
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python main.py
   ```

4. Open the application in your browser at `http://127.0.0.1:5000`.

## Usage

- Navigate to the homepage to view product details.
- Select a persona from the dropdown to customize the experience.
- Explore the "Customer Stories and Inspirations" section for AI-refined reviews.

## Contributing

Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License.