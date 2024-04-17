from flask import Flask
from flask import render_template,  redirect, url_for
from flask import Response, request, jsonify

app = Flask(__name__)

macros= [
  {
    "id": 1,
    "name": "Proteins",
    "summary": "Proteins are crucial for muscle repair and growth in bodybuilding. They provide the amino acids needed to rebuild muscle tissue that is damaged during intense workouts",
    "myth":"More protein is not always better. Excessive protein can be converted to glucose or fat if consumed in large quantities beyond what your body can use for muscle repair and growth.",
    "context":"Proteins should be balanced with carbohydrates and fats in your diet. Carbohydrates are needed for energy, and fats are vital for hormone production",
    "imp":"Proteins are the building blocks of muscle. When you lift weights, you create micro-tears in your muscle fibers. Protein helps repair these tears, which leads to muscle growth",
    "sources":"High-Quality Sources: Lean meats, poultry, fish, dairy products, eggs, and plant-based sources like beans and lentils. Supplements: Whey, casein, soy, pea, and rice protein powders.",
    "intake":"Recommendations for protein intake can vary, but a common guideline is 1.6-2.2 grams of protein per kilogram of body weight for those involved in intense training.",
    "image": "https://www.scienceforsport.com/wp-content/uploads/2020/08/Protein1-scaled.webp"
  },
  {
    "id": 2,
    "name": "Carbohydrates",
    "summary":"Carbohydrates are a key energy source for bodybuilders, fueling both high-intensity training and recovery.",
    "myth":"Carbohydrates do not make you fat by themselves. It's about the overall caloric intake and balance in your diet. Quality and timing are key for bodybuilders.",
    "context":"While carbs are essential, it's important to balance them with adequate protein for muscle repair and healthy fats for hormonal balance.",
    "imp":"Carbohydrates are the body's preferred energy source. They're stored as glycogen in muscles and the liver and are utilized during both anaerobic and aerobic exercises.",
    "sources":"Complex Carbs: Whole grains, vegetables, fruits, and legumes provide sustained energy.Simple Carbs: Fruits and certain vegetables (like carrots and beets) provide quicker energy, ideal for pre/post-workout.",
    "intake":" Recommendations can vary based on training intensity and goals, but a common guideline for bodybuilders is 4-7 grams of carbohydrates per kilogram of body weigh",
    "image": "https://medlineplus.gov/images/Carbohydrates_share.jpg"
  },
  {
    "id": 3,
    "name": "Fats",
    "summary":"Fats play a crucial role in overall health and bodybuilding by supporting metabolism, hormone production, and energy.",
    "myth":"Dietary fat is not directly related to body fat. Excess calories contribute to fat gain, not consuming fats per se.",
    "context":"Balance is key. Fats should complement your intake of proteins and carbohydrates, not replace them. Quality matters, and so does the type of fat consumed.",
    "imp":"Fats provide a concentrated source of energy, particularly important during longer or lower-intensity workouts.",
    "sources":"Healthy Fats: Avocados, nuts, seeds, olive oil, and fatty fish like salmon provide omega-3 fatty acids and monounsaturated fats. Moderate Sources: Animal fats, coconut oil, and dairy products are good in moderation and provide saturated fats, necessary in small amount",
    "intake":"A common recommendation for bodybuilders is to get about 20-35% of total daily calories from fats.",
    "image": "https://domf5oio6qrcr.cloudfront.net/medialibrary/7412/285f8582-c1c9-4d28-9174-7d77f34dd548.jpg"
  }
]

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/calc')
def calc():
    return render_template('calculate.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    lesson_data = next((lesson for lesson in macros if int(lesson['id']) == lesson_id), None)

    if lesson_data is None:
       
        return "Lesson not found", 404

    return render_template('learn.html', lesson=lesson_data)


@app.route('/calculate-macros', methods=['GET', 'POST'])
def calculate_macros():
    if request.method == 'POST':
        gender = request.form.get('gender')
        weight = float(request.form.get('weight'))  # Weight in kilograms
        height = float(request.form.get('height'))  # Height in centimeters
        age = float(request.form.get('age'))  # Age in years
        activity = request.form.get('activity')  # Activity level

        # BMR Calculation using Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Activity Level Multiplier
        activity_levels = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        activity_multiplier = activity_levels.get(activity, 1.2)

        # Total Daily Energy Expenditure (TDEE)
        tdee = round(bmr * activity_multiplier)

        # Macronutrient distribution ratios
        protein_ratio = 0.3
        fat_ratio = 0.25
        carb_ratio = 0.45

        # Macros in grams
        protein = round((tdee * protein_ratio) / 4, 1)
        fat = round((tdee * fat_ratio) / 9, 1)
        carbs = round((tdee * carb_ratio) / 4, 1)

        # Adjustments for goal
        weight_loss_calories = round(tdee * 0.85)
        bulking_calories = round(tdee * 1.15)

        # Results dictionary
        results = {
            'maintenance': {
                'calories': tdee,
                'protein': protein,
                'carbs': carbs,
                'fats': fat
            },
            'weight_loss': {
                'calories': weight_loss_calories,
                'protein': protein, 
                'carbs': round(carbs * 0.85, 1),
                'fats': round(fat * 0.85, 1)
            },
            'bulking': {
                'calories': bulking_calories,
                'protein': protein,  
                'carbs': round(carbs * 1.15, 1),
                'fats': round(fat * 1.15, 1)
            }
        }

        return render_template('result.html', results=results)

    # GET request, show the form
    return render_template('calculate.html')


@app.route('/quiz/<int:question_id>')
def quiz(question_id):
    
    return render_template('quiz1.html', question_id=question_id)

# @app.route('/quiz_result', methods=['POST'])
# def quiz_result():
#     # Process quiz answers here, e.g., calculate scores
#     # Assume answers are posted as form data
#     # Redirect to a result page with the score
#     score = calculate_score(request.form)
#     return render_template('quiz_result.html', score=score)



if __name__ == '__main__':
    app.run(debug=True)
